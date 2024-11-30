""" Testes de Validação das DAGs a serem executados em cada pipeline CI/CD. """
import logging
import os
import subprocess
import unittest

from airflow.models import Connection, DagBag
from airflow.settings import Session
from cryptography.fernet import Fernet


class TestDagIntegrity(unittest.TestCase):
    """
    Testa a integridade de cada arquivo de definição de DAG, verificando configurações padrão e formatação.
    """

    @classmethod
    def setUpClass(cls):
        """
        Antes de executar os testes, inicializamos o banco de dados do Airflow,
        criamos conexões e importamos as DAGs. Isso garante que as DAGs
        sejam totalmente integradas ao ambiente do Airflow.
        """

        # Executamos o resetdb em vez de initdb para garantir idempotência na chave Fernet.
        subprocess.run(["airflow", "db", "reset", "-y"], check=False)

        # É necessário definir uma chave Fernet para armazenar conexões no banco de dados.
        # Mais informações: https://airflow.readthedocs.io/en/stable/howto/secure-connections.html
        key = Fernet.generate_key().decode()
        os.environ["AIRFLOW__CORE__FERNET_KEY"] = key

        # Adicionamos todas as conexões ao banco de dados antes de carregar as DAGs.
        cls.session = Session()

        for connection in cls.get_connections():
            cls.session.add(connection)
            cls.session.commit()

        # Carregar as DAGs
        cls.dagbag = DagBag(dag_folder="dags", include_examples=False)
        cls.dag_ids = list(cls.dagbag.dags.keys())

    def test_import_dags(self):
        """
        Testa se todas as DAGs encontradas pelo Airflow podem ser importadas.
        """
        logging.info("DAGs a serem importadas: \n%s", "\n".join(self.dag_ids))

        self.assertFalse(
            len(self.dagbag.import_errors),
            f"Falha na importação das DAGs. Erros: {self.dagbag.import_errors}",
        )

    @classmethod
    def get_connections(cls):
        """
        Este método deve instanciar as conexões necessárias antes de executar os testes.
        Isso garante que DAGs usando conexões personalizadas possam ser importadas para testes.
        Ao criar uma nova conexão para usar em uma DAG, adicione-a aqui.
        NÃO ADICIONE INFORMAÇÕES SENSÍVEIS AQUI.
        """

        return [
            Connection(conn_id="example-connection", conn_type="http"),
        ]
