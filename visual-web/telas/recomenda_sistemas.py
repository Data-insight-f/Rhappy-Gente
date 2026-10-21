import streamlit as st

def mostrar_tela():
    st.title("🛠️ Validações na Entrada de Dados")
    st.markdown("---")
    
    st.markdown("""
    ### O papel da Governança de Dados
    Para garantir a escalabilidade do **RHappy Gente** e a precisão contínua do modelo preditivo, recomendamos que a equipe de TI e Sistemas atue em dois gargalos estruturais de arquitetura de dados na companhia:

    ---

    ### 1. Padronização Sistêmica de Nomenclaturas (Cargos)
    * **O Problema:** O sistema atual permite variações de cadastro para a mesma função operacional. O caso mais crítico ocorre na liderança, com o convívio de nomenclaturas como `GERENTE DE LOJA 1` e `GERENTE DE LOJA I`. Para o algoritmo de Inteligência Artificial, tratam-se de duas entidades completamente diferentes, o que fragmenta a análise de risco e exige regras pesadas de higienização no código (*hardcode*).
    * **A Solução Prescrita:** Travar o campo de "Cargo" no sistema de RH. A inserção não deve aceitar texto livre (*free text*), passando a operar via consulta a uma tabela de domínio único (*Master Data Management*), onde o usuário apenas seleciona a função oficial a partir de uma lista suspensa.

    ### 2. Automação de Geolocalização via API (Distância Casa-Loja)
    * **O Problema:** A coluna `distancia_loja_casa_km` apresenta baixa precisão analítica. Identificamos um padrão de agrupamento onde dezenas de colaboradores possuem a exata mesma quilometragem cadastrada. Isso indica que o preenchimento manual atual funciona por aproximação ou faixas de distância estáticas (*ranges*), reduzindo a capacidade do algoritmo de medir o desgaste logístico real na rotina do funcionário.
    * **A Solução Prescrita:** Eliminar o preenchimento manual e automatizar o cálculo de roteamento. Recomendamos que o ERP seja integrado a uma API de geolocalização (como **Google Maps Distance Matrix API** ou **OpenStreetMap / OSRM**). Ao processar o CEP residencial do colaborador e o CEP da unidade, o *back-end* calcula a distância rodoviária real de deslocamento, gravando um valor exato e confiável na base de dados.
    """)