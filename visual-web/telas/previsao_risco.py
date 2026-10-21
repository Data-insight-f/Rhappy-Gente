import streamlit as st
import pandas as pd
import joblib
import os

def mostrar_tela(df_global):
    st.title("🎯 Previsão de Risco")
    st.markdown("---")
    
    # ==========================================
    # 1. PREPARAÇÃO DA BASE (Apenas Ativos)
    # ==========================================
    df_ativos = df_global[df_global['data_demissao'].isna()].copy()
    
    if df_ativos.empty:
        st.warning("Não há colaboradores ativos na base de dados para analisar.")
        return

    # --- MALHA FINA TRIPLA (Bloqueio Total do Corporativo) ---
    # 1. Barra pela Área de Negócios (se contiver a palavra "Corporativo")
    if 'area_negocios' in df_ativos.columns:
        df_ativos = df_ativos[~df_ativos['area_negocios'].astype(str).str.contains('Corporativo', case=False, na=False)]
        
    # 2. Barra pelo Porte ou Faturamento (que padronizamos no app.py como 'Corporativo')
    if 'porte_funcionarios_loja' in df_ativos.columns:
        df_ativos = df_ativos[df_ativos['porte_funcionarios_loja'] != 'Corporativo']
        
    # 3. Barra pelo Nome da Loja Amigável (tudo que tiver "CORP" no nome)
    if 'loja_amigavel' in df_ativos.columns:
        df_ativos = df_ativos[~df_ativos['loja_amigavel'].astype(str).str.contains('CORP', case=False, na=False)]

    # ==========================================
    # 2. FILTRO INTERATIVO (Por Loja)
    # ==========================================
    st.subheader("Filtros de Atuação")
    
    lojas_unicas = list(df_ativos['loja_amigavel'].dropna().unique())
    lojas_unicas.sort()
    lista_lojas = ["Todas"] + lojas_unicas
    
    loja_selecionada = st.selectbox("Selecione a Unidade (Loja)", lista_lojas)

    # Aplica o filtro escolhido pelo usuário
    df_filtrado = df_ativos.copy()
    if loja_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['loja_amigavel'] == loja_selecionada]

    if df_filtrado.empty:
        st.info("Nenhum colaborador encontrado para a loja selecionada.")
        return

    # ==========================================
    # 3. TRATAMENTO PARA MACHINE LEARNING
    # ==========================================
    if 'resultado_raciocinio_logico' in df_filtrado.columns and 'cargo' in df_filtrado.columns:
        df_filtrado['resultado_raciocinio_logico'] = pd.to_numeric(df_filtrado['resultado_raciocinio_logico'], errors='coerce').astype('Float64')
        
        # Calculamos as medianas usando a base global (df_ativos) para evitar erros caso a loja filtrada não tenha esses cargos
        mediana_estoquista = df_ativos[df_ativos['cargo'] == 'ESTOQUISTA']['resultado_raciocinio_logico'].median()
        mediana_gerente_i = df_ativos[df_ativos['cargo'] == 'GERENTE DE LOJA I']['resultado_raciocinio_logico'].median()
        mediana_supervisor = df_ativos[df_ativos['cargo'] == 'SUPERVISOR DE LOJA']['resultado_raciocinio_logico'].median()
        
        mapa_imputacao = {
            'REPOSITOR': mediana_estoquista, 'OPERADOR DE ESTOQUE': mediana_estoquista,
            'GERENTE ASSISTENTE': mediana_gerente_i, 'COORDENADOR COMERCIAL': mediana_supervisor,
            'COORDENADOR EXPANSAO': mediana_supervisor
        }
        for cargo_alvo, valor_mediana in mapa_imputacao.items():
            mascara = df_filtrado['cargo'] == cargo_alvo
            df_filtrado.loc[mascara, 'resultado_raciocinio_logico'] = df_filtrado.loc[mascara, 'resultado_raciocinio_logico'].fillna(valor_mediana)
            
        df_filtrado['resultado_raciocinio_logico'] = df_filtrado.groupby('cargo')['resultado_raciocinio_logico'].transform(lambda x: x.fillna(x.median()))

    # ==========================================
    # 4. PREVISÃO COM XGBOOST
    # ==========================================
    pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_modelo = os.path.join(pasta_raiz, "modelo_risco.joblib")
    caminho_colunas = os.path.join(pasta_raiz, "colunas_modelo.joblib")
    
    if not os.path.exists(caminho_modelo) or not os.path.exists(caminho_colunas):
        st.error(f"⚠️ Arquivos não encontrados! O sistema procurou na pasta: {pasta_raiz}")
        return

    try:
        modelo = joblib.load(caminho_modelo)
        colunas_treino = joblib.load(caminho_colunas)

        df_encoded = pd.get_dummies(df_filtrado, drop_first=True)
        X_pred = df_encoded.reindex(columns=colunas_treino, fill_value=0)

        df_filtrado['risco_percentual'] = modelo.predict_proba(X_pred)[:, 1]

        # ==========================================
        # 5. CARDS DE IMPACTO FINANCEIRO (RISCO ALTO)
        # ==========================================
        st.markdown("---")
        st.subheader("⚠️ Impacto Financeiro (Colaboradores em Alto Risco)")
        
        # Filtramos quem a IA considera como Alto Risco (acima de 70%)
        df_alto_risco = df_filtrado[df_filtrado['risco_percentual'] > 0.70]
        qtd_alto_risco = len(df_alto_risco)
        
        # Cálculo financeiro (Salário * 1.5)
        if qtd_alto_risco > 0:
            custo_estimado_risco = (df_alto_risco['remuneracao_mensal'].sum()) * 1.5
        else:
            custo_estimado_risco = 0.0

        card1, card2 = st.columns(2)
        with card1:
            st.metric(
                label="🚨 Pessoas em Zona de Perigo (>70%)", 
                value=f"{qtd_alto_risco} colaboradores",
                help="Volume de profissionais ativos neste filtro com alta probabilidade matemática de evasão nos primeiros 90 dias."
            )
        with card2:
            custo_formatado = f"R$ {custo_estimado_risco:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            st.metric(
                label="💸 Dinheiro na Mesa (Prejuízo Potencial)", 
                value=custo_formatado,
                help="Custo estimado de reposição salário +50%(conforme benchmark de consultorias globais e nacionais: SHRM, Center for American Progress e Gupy)."
            )

        st.markdown("---")

        # ==========================================
        # 6. EXIBIÇÃO DA FILA DE AÇÃO
        # ==========================================
        st.subheader("📋 Fila de Ação (Ranking de Vulnerabilidade)")
        
        # Adicionamos os identificadores (cod_funcionario e matricula) no início da visão
        colunas_visao = ['cod_funcionario', 'matricula', 'loja_amigavel', 'cargo', 'horas_trabalhadas', 'remuneracao_mensal', 'nps_gestor', 'risco_percentual']
        
        # Garante que só vai tentar exibir as colunas se elas existirem na base
        colunas_visao = [col for col in colunas_visao if col in df_filtrado.columns]
        
        fila_acao = df_filtrado[colunas_visao].sort_values(by='risco_percentual', ascending=False).copy()
        
        # Transforma IDs em texto puro, suportando letras e números (sem forçar int)
        if 'cod_funcionario' in fila_acao.columns:
            fila_acao['cod_funcionario'] = (
                fila_acao['cod_funcionario']
                .fillna('-')
                .astype(str)
                .str.replace(r'\.0$', '', regex=True) # Tira o .0 caso tenha lido como float
            )
            
        if 'matricula' in fila_acao.columns:
            fila_acao['matricula'] = (
                fila_acao['matricula']
                .fillna('-')
                .astype(str)
                .str.replace(r'\.0$', '', regex=True)
            )
        
        st.dataframe(
            fila_acao.style.format({
                'risco_percentual': '{:.1%}',
                'remuneracao_mensal': 'R$ {:,.2f}',
                'nps_gestor': '{:.1f}'
            }).background_gradient(subset=['risco_percentual'], cmap='Reds'),
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar as previsões: {e}")