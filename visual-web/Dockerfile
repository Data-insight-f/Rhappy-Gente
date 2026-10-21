# Usa uma imagem leve do Python
FROM python:3.13-slim

# Instala o pacote de idiomas, gera o português do Brasil e limpa o cache
RUN apt-get update && apt-get install -y locales && \
    echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen pt_BR.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# Configura as variáveis de ambiente do Linux para forçar o uso do português
ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto (incluindo o app.py)
COPY . .

# Expõe a porta padrão que o Streamlit e o Cloud Run vão usar
EXPOSE 8080

# Comando para iniciar o Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]