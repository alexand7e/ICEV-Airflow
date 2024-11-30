FROM apache/airflow:2.8.1-python3.11

# root para instalar dependências
USER root

# dependências para o Google Chrome e wget e unzip
RUN apt-get update --fix-missing && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

COPY ./requirements.txt /requirements.txt

# Voltar para o usuário airflow
USER airflow

# Instalar as dependências do Python usando o pip
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
# RUN pip install --ignore-installed --force-reinstall PyMySQL

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow/dags:/opt/airflow/src"
