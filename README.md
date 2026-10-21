# RHappy Gente

Projeto de **People Analytics** e **Machine Learning** desenvolvido para monitorar e prever a evasão voluntária de colaboradores na Ri Happy. 

Este repositório contém o código-fonte da aplicação web (front-end e back-end), a estrutura do pipeline de dados, os arquivos do modelo de Inteligência Artificial serializado e as configurações de containerização.

---

## 🎯 Objetivo do Projeto

Transformar o RH de uma postura reativa para preditiva. A solução visa identificar os padrões operacionais que causam o turnover voluntário precoce (Early Attrition - primeiros 90 dias) na linha de frente das lojas. 

Através da ingestão de planilhas padrão do sistema de RH, a aplicação realiza a limpeza dos dados, calcula o impacto financeiro (Dinheiro na Mesa) e utiliza um modelo de Machine Learning (XGBoost) para gerar o ranqueamento de risco atualizado, culminando em um dossiê prescritivo individualizado para guiar a ação dos Business Partners (BPs).

---

## 📂 Estrutura do Repositório

### Diretório Principal
- `app.py`: Roteador central da aplicação Streamlit, responsável pelo upload do arquivo, limpeza em tempo real (pipeline de dados) e navegação.
- `modelo_risco.joblib`: "Cérebro" do modelo XGBoost pré-treinado e serializado.
- `colunas_modelo.joblib`: "Molde" de variáveis extraídas durante o treino para garantir consistência na inferência em produção.
- `requirements.txt`: Relação de bibliotecas Python mapeadas para a implantação.
- `Dockerfile` / `.dockerignore`: Configurações de imagem e containerização para garantir a portabilidade do ambiente entre desenvolvimento local (Ubuntu) e produção.
- `notebooks`: Jupyter Notebooks contendo a fase de *Exploratory Data Analysis* (EDA) bruta que possua dados sensíveis.

### `/telas` (Front-end e Regras de Negócio)
Contém os módulos de interface que são renderizados dinamicamente:
- `visao_historica.py`: Dashboard de análise macro e gráficos Plotly de evasões passadas.
- `previsao_risco.py`: Tabela com ranking de vulnerabilidade e cálculo financeiro do risco.
- `personas_perfis.py`: Motor de prescrição, Raio-X individual e sistema inteligente de alertas de retenção.
- `sobre.py` e `recomenda_sistemas.py`: Documentação metodológica e consultoria de governança de dados.

### 📊 PowerPoint
Contém as apresentações dos respectivos sprints(.pptx) entregues em cada etapa acadêmica do projeto.

---

## 🚫 Arquivos que NÃO ficam no repositório

Para manter a organização, conformidade com a LGPD e evitar conflitos, os seguintes arquivos não são versionados:

- Planilhas em Excel (`.xlsx`) ou CSV contendo a base bruta de funcionários da Ri Happy.
- Cache do Python (`__pycache__`).

---

## 🧱 Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface Web:** Streamlit
- **Manipulação de Dados:** Pandas, Numpy
- **Visualização:** Plotly Express
- **Machine Learning:** XGBoost, Scikit-learn (Machine Learning), Joblib (Serialização)
- **Containerização:** Docker
- **Hospedagem:** Google Cloud Run (GCP)
- **Versionamento:** Git e GitHub

---

## 🔄 Fluxo de Utilização e Arquitetura

**1. Containerização e Deploy:** A aplicação é empacotada em uma imagem Docker, utilizando o `requirements.txt` para instalar dependências e o `Dockerfile` para orquestrar o ambiente. Esse container é implantado no Google Cloud Run, garantindo escalabilidade e isolamento da infraestrutura.

**2. Upload Self-Service:** O usuário acessa a plataforma web e realiza o upload da planilha atualizada de colaboradores (`.xlsx`) diretamente no menu lateral. Não há conexão permanente com banco de dados externo.

**3. Pipeline e Malha Fina:** O script `app.py` processa o arquivo em tempo real: formata salários, trata matrículas mistas, preenche dados nulos estatísticos e aplica filtros rígidos isolando apenas o chão de loja (removendo o Corporativo da predição).

**4. Inferência do XGBoost:** Na aba de Previsão de Risco, a aplicação injeta os colaboradores ativos no modelo `joblib`, calculando instantaneamente a probabilidade (0% a 100%) de evasão de cada funcionário.

**5. Analytics Prescritivo:** Na aba de Personas e Perfis, ao buscar uma matrícula, o motor de prescrição varre o perfil da pessoa e cruza o risco com alertas como "Falta de Feedback", "Distância Casa-Loja Crítica" ou "Pressão por Metas em Lojas G4", traduzindo o risco matemático em ações práticas para o gestor de RH.

---

## 📝 Observação de Segurança (LGPD)

A aplicação **RHappy Gente** foi projetada com a premissa de *Privacy by Design*. Nenhum dado pessoal da folha de pagamento inserido via upload é armazenado, gravado em logs ou salvo em bancos de dados. Todo o processamento analítico, predição e renderização ocorre estritamente na memória volátil (RAM) da sessão ativa dentro do container. Ao recarregar a página ou fechar o navegador, os dados são permanentemente destruídos.

---

## 🪙 Custo e Prazo de Desenvolvimento do projeto

Custo Plataforma(Cliente): Google Cloud Plataform(Conta Gratuita): R$ 0,00(mensal);  
Custo Recursos Humanos: 30 dias x 4 horas por dia x 4 colaboradores = 480 horas x R$ 50,00;  
Valor Total: R$ 24.000,00.
Prazo: 30 Dias.

---

## 🔜 Próximos Passos

* Inserir exportação de relatório em pdf para os dossiês gerados na tela de Personas e Perfis.
* Verificar a possibilidade de novas análises com outros algoritmos de Machine Learning.
* Implantação das arquiteturas de integração sugeridas na tela de Evoluções do Sistema.

---

Link para acesso à aplicação: <a href="https://rhappy-gente-1067047442128.us-east1.run.app" target="_blank" rel="noopener noreferrer">RHappy Gente</a>

## 👥 Equipe

Projeto desenvolvido pela equipe Data Insight.

<table align="center" border="0" cellspacing="0" cellpadding="20">
  <tr>
    <td align="center" style="border:none;">
      <a href="https://github.com/fabioamaralds">
        <img src="./assets/imagem-fabio.png" width="100px" style="border-radius:50%;" alt="Fabio Amaral"/><br/>
        <b>Fabio Amaral</b>
      </a>
    </td>
    <td align="center" style="border:none;">
      <a href="https://github.com/ReginaBolsanelli">
        <img src="./assets/imagem-regina.png" width="100px" style="border-radius:50%;" alt="Regina Bolsanelli"/><br/>
        <b>Regina Bolsanelli</b>
      </a>
    </td>
    <td align="center" style="border:none;">
      <a href="https://github.com/tilokao1">
        <img src="./assets/imagem-thiago.png" width="100px" style="border-radius:50%;" alt="Thiago Perez"/><br/>
        <b>Thiago Perez</b>
      </a>
    </td>
    <td align="center" style="border:none;">
      <a href="https://github.com/WagnerMartins-on">
        <img src="./assets/imagem-wagner.png" width="100px" style="border-radius:50%;" alt="Wagner Santana"/><br/>
        <b>Wagner Santana</b>
      </a>
    </td>
  </tr>
</table>