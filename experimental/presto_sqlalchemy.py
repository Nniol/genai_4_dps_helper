import os
import subprocess
import sys

import pandas as pd
from ibm_watsonx_ai import APIClient
from pandas import DataFrame
from sqlalchemy import Connection, create_engine

from genai_4_dps_helper.base_obj import BaseObj


class PrestoConnection(BaseObj):
    def __init__(self, client: APIClient, server_pem_path="/tmp/presto.crt"):
        """Connects to watsonx.data Presto SQL speified in the connections property of 'client'.
        It expects the connection to be SSL and the cerficate is available in the connection metadata.

        Args:
            client (APIClient): A connected APIClient to watsonx.ai.
            server_pem_path (str, optional): Path to store the PEM file in. Defaults to "/tmp/presto.crt".
        """
        super(PrestoConnection, self).__init__()

        client_connections: DataFrame = client.connections.list()
        presto_connection_id = client_connections.loc[
            client_connections["NAME"] == "Presto", "ID"
        ].values[0]
        presto_credentials = (
            client.connections.get_details(presto_connection_id)
            .get("entity")
            .get("properties")
        )
        self.__hostname = presto_credentials["host"]
        self.__port = presto_credentials["port"]
        self.__server_pem_path = server_pem_path
        userid = presto_credentials["username"]
        password = presto_credentials["password"]
        catalog = "tpch"
        schema = "tiny"
        connect_args = {
            "protocol": "https",
            "requests_kwargs": {"verify": f"{server_pem_path}"},
        }
        # self.__get_certificate()
        # if write_cert_file:
        #     if os.path.isfile(server_pem_path):
        #         os.remove(server_pem_path)
        #     with open(server_pem_path, "a") as fp:
        #         fp.write(presto_credentials["ssl_certificate"])

        # con_str: str = f"presto://{userid}:{password}@{self.__hostname}:{self.__port}/{catalog}/{schema}"
        # print(con_str)

        self._engine = create_engine(
            f"presto://{userid}:{password}@{self.__hostname}:{self.__port}/{catalog}/{schema}",
            connect_args=connect_args,
        )

    def connect(self) -> Connection:
        return self._engine.connect()

    def select_sql(self, sql: str) -> DataFrame:
        return pd.read_sql_query(sql, self._engine)

    def insert_dataframe(
        self,
        df: DataFrame,
        schema: str,
        table: str,
        if_exists: str = "append",
        index: bool = False,
    ):
        """See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html for more info on varibale etc

        Args:
            df (DataFrame): The dataframe to load
            schema (str): The schema to load the table into
            table (str): name of the tabe
            if_exists (str, optional): What to do if the table exists, error, replace, append. Defaults to "append".
            index (bool, optional): Add an index column. Defaults to False.
        """
        return df.to_sql(name=table, con=self._engine, if_exists=if_exists, index=index)

    def __get_certificate(self):
        if os.name == "nt":
            self.__run_powershell_command()
        elif os.name == "posix":
            self.__run_linux_command()
        else:
            print(f"Running on {os.name}")

    def __run_powershell_command(self):
        command = (
            f"echo QUIT | openssl s_client -showcerts -connect {self.__hostname}:{self.__port} | awk '/-----BEGIN CERTIFICATE-----/ {{p=1}}; p; /-----END CERTIFICATE-----/ {{p=0}}' > {self.__server_pem_path}",
        )
        print(command)
        p = subprocess.Popen(
            [
                "powershell.exe",
                f"echo QUIT | openssl s_client -showcerts -connect {self.__hostname}:{self.__port} | awk '/-----BEGIN CERTIFICATE-----/ {{p=1}}; p; /-----END CERTIFICATE-----/ {{p=0}}' > {self.__server_pem_path}",
            ],
            stdout=sys.stdout,
        )
        p.communicate()

    def __run_linux_command(self):
        # process_list = [
        #     "echo",
        #     "QUIT",
        #     "|",
        #     "openssl",
        #     "s_client",
        #     "-showvcerts",
        #     "-connect",
        #     f"{self.__hostname}:{self.__port}",
        #     "|",
        #     "awk",
        #     "'/-----BEGIN CERTIFICATE-----/ {p=1}; p; /-----END CERTIFICATE-----/ {p=0}'",
        #     ">",
        #     self.__server_pem_path,
        # ]
        # print(process_list)
        import shlex

        command_line = f"echo QUIT | openssl s_client -showvcerts -connect {self.__hostname}:{self.__port} | awk '/-----BEGIN CERTIFICATE-----/ {{p=1}}; p; /-----END CERTIFICATE-----/ {{p=0}}' > {self.__server_pem_path}"
        args = shlex.split(command_line)

        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Capturing the output and errors
        stdout, stderr = process.communicate()

        # Printing the output
        print(stdout.decode(), stderr.decode())
