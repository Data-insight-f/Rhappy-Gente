import streamlit as st
import pandas as pd
import datetime


# Importando os módulos das nossas telas
from telas import visao_historica
from telas import sobre
from telas import previsao_risco
from telas import personas_perfis
from telas import recomenda_sistemas

st.set_page_config(page_title="RHappy Gente", page_icon="🧸", layout="wide")

if 'pagina_atual' not in st.session_state:
    st.session_state['pagina_atual'] = "📊 Visão Histórica"

# --- Menu Lateral ---
st.sidebar.image("logo-rhappy-gente.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.write("**Navegação**")

if st.sidebar.button("📊 Visão Histórica", use_container_width=True):
    st.session_state['pagina_atual'] = "📊 Visão Histórica"

if st.sidebar.button("🎯 Previsão de Risco", use_container_width=True):
    st.session_state['pagina_atual'] = "🎯 Previsão de Risco"

if st.sidebar.button("👥 Pessoas e Perfis", use_container_width=True):
    st.session_state['pagina_atual'] = "👥 Pessoas e Perfis"

if st.sidebar.button("ℹ️ Sobre", use_container_width=True):
    st.session_state['pagina_atual'] = "ℹ️ Sobre"

if st.sidebar.button("🛠️ Evoluções de Sistema", use_container_width=True):
    st.session_state['pagina_atual'] = "🛠️ Evoluções de Sistema"


menu = st.session_state['pagina_atual']
st.sidebar.markdown("---")
st.sidebar.header("📁 Carga de Dados")

arquivo_excel = st.sidebar.file_uploader("Insira a base de colaboradores (.xlsx)", type=["xlsx"])

@st.cache_data
def carregar_dados(arquivo):
    df = pd.read_excel(arquivo)
    
    # 1. Tratamento de Datas
    for col in ['data_admissao', 'data_demissao', 'dt_func_dat_nasc']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    # 2. Conversão de Tipos e Limpeza
    def corrigir_distancia(valor):
        if pd.isna(valor): return pd.NA
        if isinstance(valor, datetime.datetime):
            diferenca = valor - datetime.datetime(1899, 12, 31)
            return diferenca.total_seconds() / 86400.0
        try:
            return float(str(valor).replace(',', '.'))
        except:
            return pd.NA

    if 'distancia_loja_casa_km' in df.columns:
        df['distancia_loja_casa_km'] = df['distancia_loja_casa_km'].apply(corrigir_distancia)

    if 'nu_horas_base' in df.columns:
        df['nu_horas_base'] = pd.to_numeric(df['nu_horas_base'], errors='coerce').astype('Int64')

    if 'remuneracao_mensal' in df.columns:
        # Usa regex para arrancar 'R', '$', qualquer tipo de espaço e o ponto de milhar
        texto_remuneracao = (
            df['remuneracao_mensal']
            .astype(str)
            .str.replace(r'[R$\s.]', '', regex=True) 
            .str.replace(',', '.', regex=False)      
        )
        df['remuneracao_mensal'] = pd.to_numeric(texto_remuneracao, errors='coerce')

    if 'treinamentos_realizados' in df.columns:
        df['treinamentos_realizados'] = df['treinamentos_realizados'].astype(str).str.extract(r'(\d+)', expand=False).astype('Int64')

    if 'ultima_avaliacao_performance' in df.columns:
        # Substitui a vírgula brasileira por ponto antes de converter para número
        texto_nota = df['ultima_avaliacao_performance'].astype(str).str.replace(',', '.', regex=False)
        df['ultima_avaliacao_performance'] = pd.to_numeric(texto_nota, errors='coerce')

    # 3. Imputação de Mediana (Raciocínio Lógico) Essa imputação será somente para a análise preditiva
    #if 'resultado_raciocinio_logico' in df.columns and 'cargo' in df.columns:
    #    df['resultado_raciocinio_logico'] = pd.to_numeric(df['resultado_raciocinio_logico'], errors='coerce').astype('Float64')
    #    
    #    mediana_estoquista = df[df['cargo'] == 'ESTOQUISTA']['resultado_raciocinio_logico'].median()
    #    mediana_gerente_i = df[df['cargo'] == 'GERENTE DE LOJA I']['resultado_raciocinio_logico'].median()
    #    mediana_supervisor = df[df['cargo'] == 'SUPERVISOR DE LOJA']['resultado_raciocinio_logico'].median()
    #    
    #    mapa_imputacao = {
    #        'REPOSITOR': mediana_estoquista, 'OPERADOR DE ESTOQUE': mediana_estoquista,
    #        'GERENTE ASSISTENTE': mediana_gerente_i, 'COORDENADOR COMERCIAL': mediana_supervisor,
    #        'COORDENADOR EXPANSAO': mediana_supervisor
    #    }
    #    
    #    for cargo_alvo, valor_mediana in mapa_imputacao.items():
    #        mascara = df['cargo'] == cargo_alvo
    #        df.loc[mascara, 'resultado_raciocinio_logico'] = df.loc[mascara, 'resultado_raciocinio_logico'].fillna(valor_mediana)
    #        
    #    df['resultado_raciocinio_logico'] = df.groupby('cargo')['resultado_raciocinio_logico'].transform(lambda x: x.fillna(x.median()))

    # 4. Padronização de Textos (Filtros e Cargos)
    if 'cargo' in df.columns:
        df['cargo'] = df['cargo'].replace({'GERENTE DE LOJA 1': 'GERENTE DE LOJA I', 'GERENTE DE LOJA 2': 'GERENTE DE LOJA II', 'GERENTE DE LOJA 3': 'GERENTE DE LOJA III'})

    if 'faixa_grupo_faturamento' in df.columns:
        df['faixa_grupo_faturamento'] = df['faixa_grupo_faturamento'].replace({
            'G1 = Até R$ 5,799M': 'G1', 'G2 = R$ 5,800M a R$ 8,999M': 'G2',
            'G3 = R$ 9,000M a R$ 14,500M': 'G3', 'G4 = Acima de R$ 14,500M': 'G4',
            'Loja Não Inaugurada / Fechada': 'Fechada/Inativa', 'Não Classificado': 'Sem_Info_Fat',
            'Não Aplicável (Corporativo)': 'Corporativo'
        })

    if 'porte_funcionarios_loja' in df.columns:
        df['porte_funcionarios_loja'] = df['porte_funcionarios_loja'].replace({
            'Porte P (1 a 8 func)': 'Porte_P', 'Porte M (9 a 14 func)': 'Porte_M',
            'Porte G (15 a 21 func)': 'Porte_G', 'Porte GG (22+ func)': 'Porte_GG',
            'Sem Informação / Não Aplicável': 'Sem_Info_Porte', 'Corporativo / Controlada': 'Corporativo',
            'Corporativo / Matriz': 'Corporativo'
        })

# 5. Criação da Loja Amigável (Usada na Visão Histórica)
    if 'cod_loja_sap' in df.columns and 'local' in df.columns:
        # 1. Preenche vazios e converte TUDO para texto
        codigos = df['cod_loja_sap'].fillna('Sem SAP').astype(str)
        
        # 2. Remove o ".0" do final caso o Pandas tenha lido os números como float (ex: "1016.0" -> "1016")
        codigos = codigos.str.replace(r'\.0$', '', regex=True)
        
        # 3. Substitui os zeros isolados ou textos de 'nan' (caso tenham passado)
        codigos = codigos.replace(['0', 'nan', 'NAN'], 'Sem SAP')
        
        # 4. Concatena
        df['loja_amigavel'] = "(" + codigos + ") " + df['local'].astype(str)

    return df

# --- Roteador Central ---
if menu == "ℹ️ Sobre":
    # A página Sobre é documentação estática, então funciona sem Excel!
    sobre.mostrar_tela()

elif menu == "🛠️ Evoluções de Sistema":
    # A página de recomendações também é estática e funciona sem Excel!
    recomenda_sistemas.mostrar_tela()

else:
    # Para as outras páginas, verificamos se o arquivo foi carregado
    if arquivo_excel is not None:
        df_global = carregar_dados(arquivo_excel)
        
        if menu == "📊 Visão Histórica":
            visao_historica.mostrar_tela(df_global)
            
        elif menu == "🎯 Previsão de Risco":
            previsao_risco.mostrar_tela(df_global)

        elif menu == "👥 Pessoas e Perfis":
            personas_perfis.mostrar_tela(df_global)
            
    else:
        # Estado "vazio" elegante: Mostra o título da página clicada e pede o arquivo
        st.title(menu)
        st.markdown("---")
        st.info("Faça o upload da base de dados (.xlsx) no menu lateral para visualizar as análises desta página.")