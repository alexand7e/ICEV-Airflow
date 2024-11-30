# **Workshop: Airflow e Docker**

Este repositório contém o material necessário para o **Workshop sobre Airflow e Docker**, incluindo exemplos práticos de uso do Airflow para automação de workflows e a integração com Docker para facilitar o gerenciamento de dependências e ambiente.

---

## **Estrutura do Repositório**

### Diretórios

- **`_airflow`**: Configurações e arquivos essenciais para a execução do Airflow.
  - **`config`**: Arquivos de configuração do Airflow.
  - **`dags`**: Contém as DAGs definidas para os exemplos do workshop.
    - **`dag_auto.py`**: Exemplo principal de DAG automatizada com etapas para integração de APIs e manipulação de dados.
  - **`logs`**: Diretório onde os logs de execução das DAGs são armazenados.
  - **`plugins`**: Extensões ou operadores personalizados para o Airflow.

- **`data`**: Diretório para armazenar dados gerados ou utilizados pelas DAGs.
  - **`generated_article.txt`**: Arquivo de saída criado por uma das DAGs como exemplo.

- **`notebooks`**: Notebooks interativos (Jupyter) usados para complementar a explicação teórica do workshop.

- **`src`**: Código-fonte das funções auxiliares utilizadas pelas DAGs.
  - **`app/auto.py`**: Contém classes e funções principais para integração com APIs e processamento.
  - **`db/postgres.py`**: Scripts para manipulação de banco de dados PostgreSQL.

- **`tests`**: Scripts de testes para verificar a funcionalidade das DAGs e módulos.

### Arquivos

- **`.env`**: Arquivo para configuração de variáveis de ambiente (API keys, credenciais do banco, etc.).
- **`.gitignore`**: Define os arquivos e diretórios a serem ignorados pelo Git.
- **`docker-compose.yaml`**: Configuração do Docker Compose para inicializar o ambiente do Airflow.
- **`dockerfile`**: Configuração do container Docker personalizado para o Airflow.
- **`Makefile`**: Comandos automatizados para configuração e execução do projeto.
- **`requirements.txt`**: Lista de dependências Python para o Airflow e os módulos auxiliares.
- **`setup.py`**: Configuração do pacote Python usado no projeto.
- **`variables.json`**: Arquivo de variáveis para configuração do Airflow via CLI.

---

## **Pré-requisitos**

1. **Docker** e **Docker Compose**:
   - Certifique-se de que o Docker e o Docker Compose estão instalados no sistema.

2. **Python** (opcional para customizações):
   - Versão 3.8 ou superior.

---

## **Como Executar**

### 1. Clone o Repositório

```bash
git clone https://github.com/alexand7e/ICEV-airflow.git
cd ICEV-airflow
```

### 2. Configure as Variáveis de Ambiente

- Crie um arquivo `.env` com as seguintes variáveis (exemplo):
  ```env
  GEMINI_API_KEY=<sua_api_key>
  NEWS_API_KEY=<sua_api_key>
  DB_USER=<usuario_banco>
  DB_PASSWORD=<senha_banco>
  DB_HOST=localhost
  DB_NAME=airflow_db
  DB_PORT=5432
  ```

### 3. Inicialize o Ambiente com Docker Compose

- Execute o comando para subir o ambiente:
  ```bash
  docker-compose up -d
  ```

- O Airflow estará disponível em: `http://localhost:8080`.

### 4. Acesse o Airflow

1. Faça login com:
   - **Usuário**: `airflow`
   - **Senha**: `airflow`
2. Ative e execute as DAGs no painel do Airflow.

---

## **Objetivo do Workshop**

1. Demonstrar o uso do **Apache Airflow** para agendamento e automação de workflows.
2. Configurar o **Docker** para facilitar o setup do ambiente Airflow.
3. Criar DAGs que:
   - Integram APIs externas (Google Trends, NewsAPI).
   - Processam e armazenam dados em um banco PostgreSQL.
   - Geram arquivos de saída (.txt) com resultados.

---

## **Principais Componentes do Workshop**

### **DAGs**
- **`dag_auto.py`**:
  - Pipeline completo que:
    1. Busca tendências do Google Trends.
    2. Obtém notícias relacionadas via NewsAPI.
    3. Gera artigos jornalísticos com o Gemini AI.
    4. Salva o resultado em um arquivo `.txt`.

### **Docker**
- Configuração pronta para:
  - Inicializar o Airflow com `PostgreSQL` como backend.
  - Facilitar o desenvolvimento sem configurar dependências manualmente.

### **Banco de Dados**
- Scripts para criar e gerenciar tabelas no PostgreSQL.

---

## **Comandos Úteis**

- **Parar o Ambiente**:
  ```bash
  docker-compose down
  ```

- **Reiniciar o Airflow**:
  ```bash
  docker-compose restart
  ```

- **Executar Testes**:
  ```bash
  pytest tests/
  ```

---

## **Licença**

Este projeto está licenciado sob a **MIT License**.

---

## **Contribuição**

Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias no repositório. 🚀

---

Com isso, você tem uma explicação completa e pronta para um workshop sobre **Airflow** e **Docker**!