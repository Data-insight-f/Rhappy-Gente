import streamlit as st
import pandas as pd
import joblib
import os

def mostrar_tela(df_global):
    st.title("👥 Raio-X do Colaborador")
    st.markdown("---")
    
    # ==========================================
    # 1. PREPARAÇÃO (Apenas Ativos do Varejo)
    # ==========================================
    df_ativos = df_global[df_global['data_demissao'].isna()].copy()
    
    # Malha Fina do Varejo
    if 'area_negocios' in df_ativos.columns:
        df_ativos = df_ativos[~df_ativos['area_negocios'].astype(str).str.contains('Corporativo', case=False, na=False)]
    if 'porte_funcionarios_loja' in df_ativos.columns:
        df_ativos = df_ativos[df_ativos['porte_funcionarios_loja'] != 'Corporativo']
    if 'loja_amigavel' in df_ativos.columns:
        df_ativos = df_ativos[~df_ativos['loja_amigavel'].astype(str).str.contains('CORP', case=False, na=False)]

    if df_ativos.empty:
        st.warning("Não há colaboradores ativos nas lojas para analisar.")
        return

    # Limpeza da Matrícula
    if 'matricula' in df_ativos.columns:
        df_ativos['matricula'] = df_ativos['matricula'].fillna('-').astype(str).str.replace(r'\.0$', '', regex=True)

    # ==========================================
    # 2. BUSCA DO COLABORADOR (EXATA)
    # ==========================================
    st.subheader("🔍 Selecione o Colaborador")
    st.write("Digite a matrícula exata para abrir o diagnóstico de retenção.")
    
    # Troca o Selectbox (que faz busca aproximada) pelo Text Input (busca exata)
    matricula_buscada = st.text_input(
        "Matrícula do Colaborador:", 
        placeholder="Ex: MAT_123456"
    )
    
    if not matricula_buscada:
        st.info("👆 Digite uma matrícula no campo acima e aperte Enter para gerar o dossiê.")
        return
    
    # Remove espaços vazios do início/fim e filtra pela correspondência EXATA
    matricula_limpa = matricula_buscada.strip()
    df_pessoa = df_ativos[df_ativos['matricula'] == matricula_limpa].copy()
    
    if df_pessoa.empty:
        st.warning(f"⚠️ Nenhuma pessoa ativa encontrada com a matrícula exata '{matricula_limpa}'. Verifique se digitou corretamente.")
        return

    # ==========================================
    # 3. CÁLCULO DE RISCO (Consistência com Previsão)
    # ==========================================
    pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_modelo = os.path.join(pasta_raiz, "modelo_risco.joblib")
    caminho_colunas = os.path.join(pasta_raiz, "colunas_modelo.joblib")
    
    risco_calculado = 0.0
    
    if os.path.exists(caminho_modelo) and os.path.exists(caminho_colunas):
        modelo = joblib.load(caminho_modelo)
        colunas_treino = joblib.load(caminho_colunas)
        
        # 1. Trata a base inteira
        if 'resultado_raciocinio_logico' in df_ativos.columns:
            df_ativos['resultado_raciocinio_logico'] = pd.to_numeric(df_ativos['resultado_raciocinio_logico'], errors='coerce').fillna(0)
            
        # 2. Faz o dummies na base GLOBAL 
        df_encoded = pd.get_dummies(df_ativos, drop_first=True)
        X_pred = df_encoded.reindex(columns=colunas_treino, fill_value=0)
        
        # 3. Calcula o risco de todo mundo
        df_ativos['risco_percentual'] = modelo.predict_proba(X_pred)[:, 1]
        
        # 4. AGORA extraímos a linha EXATA pela matrícula
        df_pessoa_atualizada = df_ativos[df_ativos['matricula'] == matricula_limpa]
        risco_calculado = df_pessoa_atualizada['risco_percentual'].iloc[0]

    # ==========================================
    # 4. O DOSSIÊ E O MOTOR DE PRESCRIÇÃO
    # ==========================================
    st.markdown("---")
    st.subheader("📋 Diagnóstico e Ação Recomendada")
    
    col1, col2 = st.columns([1, 2])
    
    # Usamos a linha da base atualizada para manter a sincronia perfeita dos dados
    linha_colaborador = df_pessoa_atualizada.iloc[0]
    
    # Tratamento elegante para exibir a Data de Admissão no formato brasileiro
    if pd.notna(linha_colaborador['data_admissao']):
        data_admissao_str = linha_colaborador['data_admissao'].strftime('%d/%m/%Y')
    else:
        data_admissao_str = "Não registrada"
    
    with col1:
        st.metric(label="Risco de Evasão (90 dias)", value=f"{risco_calculado:.1%}")
        st.write(f"**Matrícula:** {linha_colaborador['matricula']}")
        st.write(f"**Data de Admissão:** {data_admissao_str}") 
        st.write(f"**Cargo:** {linha_colaborador['cargo']}")
        st.write(f"**Unidade:** {linha_colaborador['loja_amigavel']}")
        
        # --- CÓDIGO DO GERENTE ---
        # Como é alfanumérico e sempre preenchido, basta puxar direto convertendo para texto
        cod_gerente = linha_colaborador.get('codigo_gerente', 'Não informado')
        st.write(f"**Cód. Gerente Imediato:** {str(cod_gerente)}")
        
        st.write(f"**Remuneração:** R$ {linha_colaborador['remuneracao_mensal']:,.2f}")
        
        # --- NOTA DE PERFORMANCE ---
        nota_perf = linha_colaborador.get('ultima_avaliacao_performance', pd.NA)
        if pd.isna(nota_perf):
            texto_nota = "Não avaliado"
        else:
            texto_nota = f"{nota_perf}" if isinstance(nota_perf, str) else f"{float(nota_perf):g}"
            
        st.write(f"**Última Avaliação:** {texto_nota}")
        
    with col2:
        st.markdown("#### 🚨 Alertas de Vulnerabilidade")
        
        # Extrai os dados reais da pessoa para as regras
        distancia = pd.to_numeric(linha_colaborador['distancia_loja_casa_km'], errors='coerce')
        nps = pd.to_numeric(linha_colaborador['nps_gestor'], errors='coerce')
        fat = linha_colaborador['faixa_grupo_faturamento']
        porte = linha_colaborador['porte_funcionarios_loja']
        
        # Correção: Lógica segura para descobrir se está sem avaliação
        if 'sem_avaliacao_formal' in df_pessoa_atualizada.columns:
            sem_aval = linha_colaborador['sem_avaliacao_formal']
        else:
            nota_performance = linha_colaborador.get('ultima_avaliacao_performance', pd.NA)
            sem_aval = 1 if pd.isna(nota_performance) else 0
            
        alertas_disparados = 0
        
        # Regra 1: Distância Crítica
        if pd.notna(distancia) and distancia > 15:
            st.warning(f"🚗 **Distância Crítica ({distancia:.1f} km):** Estudar transferência para unidade mais próxima.")
            alertas_disparados += 1
            
        # Regra 2: Gestão Fraca
        if pd.notna(nps) and nps < 60:
            st.warning(f"📉 **NPS do Gestor Baixo ({nps}):** Conduzir entrevista de escuta (skip-level) para mapear a raiz da insatisfação de forma segura.")
            alertas_disparados += 1
            
        # Regra 3: Falta de Avaliação (Apenas para quem tem mais de 12 meses de casa)
        if sem_aval == 1:
            if pd.notna(linha_colaborador['data_admissao']):
                # Calcula a diferença de dias entre hoje e a admissão, e divide por 30
                dias_no_escuro = (pd.Timestamp.now() - linha_colaborador['data_admissao']).days
                meses_no_escuro = max(0, dias_no_escuro // 30)
                
                # A mágica acontece aqui: O alerta só entra na tela se tiver mais de 1 ano (12 meses)
                if meses_no_escuro > 12:
                    st.warning(f"🙈 **Falta de Feedback:** Colaborador operando no escuro há {meses_no_escuro} meses. Cobrar urgente avaliação de desempenho.")
                    alertas_disparados += 1
                    
            else:
                # Fallback de segurança (caso algum dia o RH esqueça de preencher a data)
                st.warning("🙈 **Falta de Feedback:** Colaborador sem avaliação e sem data de admissão no sistema. Cobrar urgente avaliação de desempenho.")
                alertas_disparados += 1
            
        # Regra 4: Pressão G4
        if risco_calculado > 0.70 and fat == 'G4':
            st.error("🏢 **Risco Alto + Loja G4:** Unidade de altíssimo faturamento. Avaliar estresse ocupacional ou pressão severa por metas.")
            alertas_disparados += 1
            
        # Regra 5: Risco Sistêmico Porte P
        if risco_calculado > 0.70 and porte == 'Porte_P':
            st.error("⚠️ **ALERTA CRÍTICO:** Unidade de pequeno porte (1 a 8 func). A saída deste colaborador compromete gravemente a escala operacional da loja. Retenção imediata.")
            alertas_disparados += 1
            
        # Fechamento Dinâmico
        if alertas_disparados == 0:
            if risco_calculado >= 0.50:
                st.warning("⚠️ **Risco Sistêmico do Perfil:** A alta probabilidade de evasão está atrelada à combinação de cargo, carga horária e remuneração, mesmo sem anomalias isoladas (como distância ou notas baixas). \n\n**Ação:** Conduzir 'Entrevista de Permanência' (Stay Interview) focada em plano de carreira, expectativas financeiras e adequação da jornada.")
            else:
                st.success("✅ O colaborador apresenta baixo risco de evasão e nenhum alerta de vulnerabilidade isolada foi mapeado. Cenário estabilizado.")