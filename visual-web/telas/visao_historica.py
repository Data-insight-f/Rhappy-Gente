import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_tela(df_global):
    st.title("📊 Visão Histórica")
    st.write("Análise do impacto financeiro e volume de saídas voluntárias")
    st.markdown("---")
    
    # ==========================================
    # 1. MOTOR DE FILTRO GLOBAL (Back-end)
    # ==========================================
    # Filtra apenas quem saiu da empresa
    df_saidas = df_global[df_global['data_demissao'].notna()].copy()
    
    # Se a coluna de motivo existir, filtra apenas os pedidos de demissão (ajuste o texto exato se necessário)
    if 'desc_motivo_rescisao' in df_saidas.columns:
        df_saidas = df_saidas[df_saidas['desc_motivo_rescisao'].astype(str).str.contains('Empregado', case=False, na=False)]

    # ==========================================
    # 2. FILTROS INTERATIVOS DA TELA (Front-end)
    # ==========================================
    st.subheader("Filtros de Análise")
    
    # Agora dividimos em 4 colunas em vez de 3
    filtro_col1, filtro_col2, filtro_col3, filtro_col4 = st.columns(4)
    
    with filtro_col1:
        # 1. Extrai as áreas e ordena alfabeticamente PRIMEIRO
        areas_unicas = list(df_saidas['area_negocios'].dropna().unique())
        areas_unicas.sort()
        
        # 2. DEPOIS adiciona o "Todas" no início para ele ser o índice 0 (padrão)
        lista_areas = ["Todas"] + areas_unicas
        area_selecionada = st.selectbox("Área de Negócio", lista_areas)
        
    with filtro_col2:
        # Filtro em Cascata
        if area_selecionada == "Todas":
            df_lojas_disponiveis = df_saidas
        else:
            df_lojas_disponiveis = df_saidas[df_saidas['area_negocios'] == area_selecionada]
            
        # Mesmo truque: ordena as lojas primeiro, depois coloca o "Todas" no topo
        lojas_unicas = list(df_lojas_disponiveis['loja_amigavel'].dropna().unique())
        lojas_unicas.sort()
        
        lista_lojas = ["Todas"] + lojas_unicas
        loja_selecionada = st.selectbox("Loja", lista_lojas)
        
    with filtro_col3:
        lista_faturamento = ["Todos"] + list(df_saidas['faixa_grupo_faturamento'].dropna().unique())
        faturamento_selecionado = st.selectbox("Faixa de Faturamento", lista_faturamento)
        
    with filtro_col4:
        lista_porte = ["Todos"] + list(df_saidas['porte_funcionarios_loja'].dropna().unique())
        porte_selecionado = st.selectbox("Porte da Loja", lista_porte)

    # Aplicando as seleções na base de dados (Funil de filtragem)
    df_filtrado = df_saidas.copy()
    
    if area_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['area_negocios'] == area_selecionada]
    if loja_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['loja_amigavel'] == loja_selecionada]
    if faturamento_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['faixa_grupo_faturamento'] == faturamento_selecionado]
    if porte_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['porte_funcionarios_loja'] == porte_selecionado]

    st.markdown("---")

    # ==========================================
    # 3. CÁLCULO DOS INDICADORES (Cards)
    # ==========================================
    total_saidas = len(df_filtrado)
    
    # Proteção caso a base filtrada fique vazia
    if total_saidas > 0:
        # Custo = (Salário * 1.5). Precisamos garantir que remuneracao_mensal seja número
        df_filtrado['remuneracao_mensal'] = pd.to_numeric(df_filtrado['remuneracao_mensal'], errors='coerce').fillna(0)
        custo_turnover = (df_filtrado['remuneracao_mensal'] * 1.5).sum()
        
        # Mês com maior evasão (Sazonalidade)
        df_filtrado['data_demissao'] = pd.to_datetime(df_filtrado['data_demissao'], errors='coerce')
        mes_pico = df_filtrado['data_demissao'].dt.month_name(locale='pt_BR.utf8').mode()[0].capitalize() if not df_filtrado['data_demissao'].isna().all() else "N/A"
    else:
        custo_turnover = 0
        mes_pico = "N/A"

    # ==========================================
    # 4. EXIBIÇÃO DOS CARDS
    # ==========================================
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🚪 Total de Saídas Voluntárias", 
            value=f"{total_saidas:,}".replace(',', '.'),
            help="Número total de colaboradores que pediram demissão no cenário filtrado."
        )
        
    with col2:
        st.metric(
            label="📅 Mês com Maior Evasão", 
            value=mes_pico,
            help="Mês que concentra o maior volume histórico de rescisões voluntárias."
        )
        
    with col3:
        custo_formatado = f"R$ {custo_turnover:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        st.metric(
            label="💸 Custo Histórico Estimado", 
            value=custo_formatado,
            help="Valor total da remuneração mensal dos colaboradores que solicitaram demissão voluntária, com um acréscimo de 50% (conforme benchmark de consultorias globais e nacionais: SHRM, Center for American Progress e Gupy)."
        )
        
    st.markdown("---")
    # ==========================================
    # 5. ANÁLISE GRÁFICA (Visualizações)
    # ==========================================
    # Você também pode colocar um 'help' no subtítulo geral!
    st.subheader("📈 Dinâmica de Evasão", help="Volume do total de saídas voluntárias distribuídas no mês.")
    
    graf_col1, graf_col2 = st.columns(2)
    
    with graf_col1:
        st.markdown("**Curva Histórica de Saídas**", help="Acompanha o volume de pedidos de demissão ao longo do tempo, ajudando a identificar picos de sazonalidade (ex: excesso de saídas pós-Natal).")
        
        df_filtrado['mes_ano'] = df_filtrado['data_demissao'].dt.to_period('M').astype(str)
        evasao_mes = df_filtrado[df_filtrado['mes_ano'] != 'NaT'].groupby('mes_ano').size().reset_index(name='saidas')
        
        fig_linha = px.line(evasao_mes, x='mes_ano', y='saidas', markers=True,
                            labels={'mes_ano': 'Mês/Ano', 'saidas': 'Volume de Evasão'},
                            color_discrete_sequence=['#00b3e3'])
        # Reduz a margem do topo já que tiramos o title interno do px.line
        fig_linha.update_layout(margin=dict(t=10)) 
        st.plotly_chart(fig_linha, use_container_width=True)

    with graf_col2:
        st.markdown("**Top 10 Lojas Críticas**", help="Ranking das unidades com o maior número de saídas voluntárias registradas.")
        
        top_lojas = df_filtrado.groupby('loja_amigavel').size().reset_index(name='saidas')
        top_lojas = top_lojas.sort_values(by='saidas', ascending=False).head(10)
        
        fig_barras = px.bar(top_lojas, x='saidas', y='loja_amigavel', orientation='h',
                            labels={'loja_amigavel': 'Unidade (SAP e Nome)', 'saidas': 'Total de Saídas'},
                            color_discrete_sequence=['#ff4b4b'])
        fig_barras.update_layout(yaxis={'categoryorder': 'total ascending'}, margin=dict(t=10)) 
        st.plotly_chart(fig_barras, use_container_width=True)

    st.markdown("---")
    
    # ==========================================
    # 6. DISTRIBUIÇÃO POR PERFIL DE LOJA [NOVO V2]
    # ==========================================
    graf_col3, graf_col4 = st.columns(2)
    
    with graf_col3:
        st.markdown("**Saídas por Porte de Funcionários**", help="Mostra se a evasão está mais concentrada em lojas pequenas (Porte P) ou grandes (Porte GG), indicando potenciais problemas na escala de trabalho.")
        
        evasao_porte = df_filtrado.groupby('porte_funcionarios_loja').size().reset_index(name='saidas')
        fig_rosca_porte = px.pie(evasao_porte, values='saidas', names='porte_funcionarios_loja', hole=0.4)
        fig_rosca_porte.update_layout(margin=dict(t=10))
        st.plotly_chart(fig_rosca_porte, use_container_width=True)

    with graf_col4:
        st.markdown("**Saídas por Faixa de Faturamento**", help="Mapeia o risco de evasão em relação à pressão por metas da loja (G1 = Menor Faturamento, G4 = Altíssimo Faturamento).")
        
        evasao_fat = df_filtrado.groupby('faixa_grupo_faturamento').size().reset_index(name='saidas')
        fig_rosca_fat = px.pie(evasao_fat, values='saidas', names='faixa_grupo_faturamento', hole=0.4)
        fig_rosca_fat.update_layout(margin=dict(t=10))
        st.plotly_chart(fig_rosca_fat, use_container_width=True)
        st.markdown("---")
    
    # ==========================================
    # 7. TABELA DE DADOS DETALHADA
    # ==========================================
    st.subheader("📋 Detalhamento dos Registros", help="Visão tabular de todos os colaboradores que compõem os gráficos acima. Clique no cabeçalho das colunas para ordenar ou no ícone de download (no canto superior direito da tabela) para exportar os dados.")
    
    # Opcional: Se a tabela tiver colunas demais, você pode filtrar quais quer mostrar.
    # Exemplo: df_exibicao = df_filtrado[['loja_amigavel', 'cargo', 'data_admissao', 'data_demissao', 'remuneracao_mensal']]
    # Aqui, vamos mostrar todas as colunas disponíveis:
    
    st.dataframe(
        df_filtrado, 
        use_container_width=True, 
        hide_index=True # Oculta aquela coluna inútil de números (0, 1, 2, 3...) na lateral
    )