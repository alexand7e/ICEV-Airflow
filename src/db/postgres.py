# Dependências
from psycopg2 import (Error, sql)
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class PostgreSQL:
    """
    Esta classe estabelece e gerencia a conexão com um banco de dados PostgreSQL.
    """
    def __init__(self, default_connection: bool = True, 
                 user: str = None, 
                 passw: str = None, 
                 host: str = None, 
                 database: str = None, 
                 port: str = None,
                 schema: str = "public"):
        
        if default_connection:
            # Usar credenciais do .env
            self.user = os.getenv('DB_USER')
            self.password = os.getenv('DB_PASSWORD')
            self.host = os.getenv('DB_HOST')
            self.db = os.getenv('DB_NAME')
            self.port = os.getenv('DB_PORT')
        else:
            self.user = user
            self.password = passw
            self.host = host
            self.db = database
            self.port = port

        self.schema = self.set_schema(schema)
        self.connector = self._connection()

    def _connection(self):
        try:
            cnx = psycopg2.connect(user=self.user, 
                                   password=self.password,
                                   host=self.host,
                                   dbname=self.db,
                                   port=self.port,
                                   options='-c client_encoding=utf8')
            print("Conexão com o banco de dados estabelecida com sucesso.")
            return cnx
        except Error as e:
            print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
            return None


    def table_exists(self, 
                     table_name: str) -> bool:
        
        query = sql.SQL("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = {} AND table_name = {})").format(
            sql.Literal(self.schema),
            sql.Literal(table_name)
        )

        cursor = self.connector.cursor()
        cursor.execute(query)
        exists = cursor.fetchone()[0]
        cursor.close()

        return exists   


    def create_table(self, 
                     table_name: str, 
                     df: pd.DataFrame, 
                     adjust_dataframe: bool = True) -> None:
        
        full_table_name = f'{self.schema}.{table_name}'
        
        if df is None:
            raise ValueError("O DataFrame 'df' é None antes de chamar create_table.")
        else:
            print(f"DataFrame tem {len(df)} linhas e {len(df.columns)} colunas antes de chamar create_table.")

        try:
            cursor = self.connector.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {full_table_name}")

            cursor.execute(f'CREATE TABLE {full_table_name} (indice SERIAL PRIMARY KEY)')

            if adjust_dataframe:
                df = self.I.normalizar_colunas(df)

            column_data_types = ['TEXT'] * len(df.columns)

            # Adicionando colunas à tabela
            for col, data_type in zip(df.columns, column_data_types):
                col_query = sql.SQL("ALTER TABLE {} ADD COLUMN {} {}").format(
                    sql.Identifier(self.schema, table_name),
                    sql.Identifier(col),
                    sql.SQL(data_type)
                )
                cursor.execute(col_query)

            # Inserindo dados na tabela
            for row in df.itertuples(index=False):
                valores = tuple(row)
                colunas = sql.SQL(', ').join([sql.Identifier(c) for c in df.columns])
                placeholders = sql.SQL(', ').join(sql.Placeholder() * len(df.columns))
                insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(self.schema, table_name),
                    colunas,
                    placeholders
                )
                cursor.execute(insert_query, valores)

            self.connector.commit()
            cursor.close()

        except Error as e:
            print(f"Erro ao criar ou recriar a tabela: {e}")


    def insert_into_table(self, 
                          table_name: str, 
                          df: pd.DataFrame,
                          adjust_dataframe: bool = True) -> None:
        """
        Insert DataFrame into a PostgreSQL table.
        """
        if adjust_dataframe:
            df = self.I.normalizar_colunas(df)
        if self.table_exists(table_name):
            try:
                cursor = self.connector.cursor()
                # Generate column identifiers
                colunas = sql.SQL(', ').join([sql.Identifier(c) for c in df.columns])
                # Generate placeholders for each column
                placeholders = sql.SQL(', ').join(sql.Placeholder() for _ in df.columns)  # Corrected line
                insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(self.schema, table_name),
                    colunas,
                    placeholders
                )
                # Execute insert query for each row
                for row in df.itertuples(index=False):
                    valores = tuple(row)
                    cursor.execute(insert_query, valores)
                self.connector.commit()
                cursor.close()
            except Exception as e:  # Changed from Error to Exception for a broader catch
                print(f"Erro ao inserir dados na tabela: {e}")
        else:
            print(f"A tabela '{table_name}' não existe.")


    def execute_query(self, query: str) -> None:
        """
        Executa uma query SQL fornecida como uma string.

        Args:
        query (str): A query SQL para ser executada.

        Raises:
        ValueError: Se a query é None ou uma string vazia.
        """
        if not query:
            raise ValueError("A query fornecida está vazia ou é None.")

        try:
            cursor = self.connector.cursor()
            cursor.execute(query)
            self.connector.commit()
            print("Query executada com sucesso.")
        except Error as e:
            print(f"Erro ao executar a query: {e}")
        finally:
            cursor.close()

