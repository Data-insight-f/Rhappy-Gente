import streamlit as st

def mostrar_tela():
    st.title("ℹ️ Sobre o RHappy Gente")
    st.markdown("---")
    
    st.markdown("""
    ### Por que este projeto existe
    A gestão de rotatividade (turnover) no varejo costuma ser reativa: o RH só age quando a carta de demissão já está na mesa. O **RHappy Gente** nasceu da necessidade de mudar essa dinâmica. 
    
    A ideia era parar de olhar apenas pelo retrovisor e começar a prever a "fuga de talentos" usando os próprios dados do sistema de RH. Transformamos os registros históricos de contratações, avaliações e demissões em um grande modelo de Inteligência Artificial (XGBoost) capaz de identificar quem está na "zona de perigo" e prescrever ações antes que o colaborador decida sair. Virou um verdadeiro radar de retenção para a linha de frente.

    ---

    ### Termos e Categorias
    Para garantir a precisão matemática do painel, estabelecemos cortes específicos nos dados:

    * **Turnover Voluntário:** A Inteligência Artificial ignora demissões feitas pela empresa ou fins de contrato. O foco é 100% em quem **pediu demissão** (*"Sem justa causa iniciativa do empregado"*).
    * **Early Attrition (Evasão Precoce):** O modelo preditivo foi treinado para caçar falhas de *onboarding* e choque cultural, prevendo quem tem maior chance de desistir nos seus **primeiros 90 dias**.
    * **Custo Histórico (1.5x):** O impacto financeiro não é um chute. É um *benchmark* conservador de mercado (SHRM, Gupy, CAP) que adiciona 50% ao salário mensal para cobrir os "custos invisíveis" da saída: exames rescisórios, tempo de recrutamento e a quebra brusca de produtividade da loja.
    * **Dinheiro na Mesa:** Na tela de previsão, o sistema isola automaticamente os colaboradores em **Alto Risco (> 70%)** e calcula o prejuízo potencial imediato caso a empresa não tome ações de retenção.
    * **Isolamento de Varejo:** Dinâmicas de matriz (Corporativo) e chão de loja são opostas. O painel histórico mostra a empresa toda, mas a IA foi blindada por uma "Malha Fina Tripla" para focar exclusivamente no comportamento das **Lojas**.

    ---

    ### Como o risco é medido e tratado
    A IA não usa bola de cristal, usa estatística. O algoritmo **XGBoost** cruza dezenas de variáveis do colaborador ativo (carga horária, distância, salário, nota do gestor, faturamento da unidade) e compara com o DNA de ex-funcionários da Ri Happy que tinham o mesmo perfil e pediram demissão no passado.
    
    Durante o processamento (*Pipeline de Dados*), o aplicativo corrige inconsistências sistêmicas comuns: padroniza matrículas com textos misturados (ex: `FUNC_123`), alinha formatos financeiros e preenche lacunas estatísticas (como testes lógicos não aplicados) usando a mediana do cargo, garantindo que o modelo nunca engasgue ao vivo.

    ---

    ### O Motor de Prescrição (Analytics Acionável)
    O grande diferencial tecnológico da plataforma está na aba *Raio-X do Colaborador*. O sistema não entrega apenas a probabilidade de saída, ele varre os dados individuais e gera um **Dossiê Automático** guiando o Business Partner (BP) do RH sobre o que fazer:
    
    1. **Distância Crítica (> 15km):** Prescreve a possibilidade de transferência de unidade.
    2. **NPS do Gestor Baixo (< 60):** Alerta para a condução de uma entrevista de escuta segura (*skip-level*), evitando conflitos diretos imediatos com a liderança.
    3. **Falta de Feedback:** Calcula há quantos meses o colaborador está na empresa. Se ultrapassar 12 meses sem avaliação formal, dispara cobrança à liderança.
    4. **Pressão G4 e Porte P:** Se o colaborador estiver em Alto Risco (>70%), a IA cruza com o tamanho da loja. Lojas G4 geram alertas de estresse ocupacional por metas agressivas, enquanto Lojas Porte P (pequenas) geram Alertas Críticos de risco de quebra na escala operacional.
    5. **Entrevista de Permanência (Stay Interview):** Se o risco for superior a 50%, mas sem anomalias visíveis, a ferramenta diagnostica que a dor é sistêmica (exaustão pelo cargo ou salário) e orienta uma conversa de alinhamento de expectativas.

    ---

    ### Histórico de Versões
    O que mudou no painel desde o escopo inicial:
    * **V3 · Raio-X e Motor de Prescrição:** Lançamento da aba *Personas e Perfis* com busca exata por matrícula e dossiê prescritivo individualizado.
    * **V2 · Fila de Ação Preditiva:** Tela de Previsão de Risco com ranqueamento interativo de vulnerabilidade (probabilidade da IA), integração do arquivo congelado `.joblib` e cálculo de impacto financeiro (Dinheiro na Mesa). Filtros em cascata dinâmicos.
    * **V1 · Pipeline e Visão Histórica:** Criação do roteador central (`app.py`), higienização profunda dos dados de RH e consolidação dos gráficos de impacto financeiro macro da companhia.

    ---

    ### Quem fez
    Desenvolvido pela equipe **Data Insight**, estudantes de Data Science e Big Data Architecture na FIAP. Com background em engenharia de dados e automação no setor de telecomunicações, este projeto une arquitetura de dados escalável com estratégias reais de *Business Intelligence* e *Machine Learning* focadas em gestão executiva de talentos.
    """)