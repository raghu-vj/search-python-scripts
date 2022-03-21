import logging.config

import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

SNOWFLAKE_USER = 'search.dev@swiggy.in'
SNOWFLAKE_ACCOUNT = 'swiggy-caifuhmyskbpytwlscdfskwp3sfya.global'
SNOWFLAKE_WAREHOUSE = 'ENGG_WH_01'
SNOWFLAKE_ROLE = 'SEARCH_ENGG'
SNOWFLAKE_DATABASE = 'DATA_SCIENCE'
SNOWFLAKE_SCHEMA = 'ITEM_EMBEDDINGS_SIAMESE_TRIPLET_64DIM_V1'

class SnowflakeClient:

    connection = None

    def get_connection(self):
        if self.connection is not None:
            return self.connection
        with open('snowflake_key.pem', "rb") as key:
            p_key = serialization.load_pem_private_key(
                key.read(),
                password=None,
                backend=default_backend()
            )

        pkb = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        self.connection = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            account=SNOWFLAKE_ACCOUNT,
            private_key=pkb,
            warehouse=SNOWFLAKE_WAREHOUSE,
            role=SNOWFLAKE_ROLE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        return self.connection

    def fetch_results(self, query):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            conn.rollback()
