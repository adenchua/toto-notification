import logging

from opensearchpy import OpenSearch

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)


class DatabaseService:
    def __init__(self, host: str, username: str, password: str):
        auth = (username, password)
        self.client = OpenSearch(
            hosts=[{"host": host}],
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
        )

        try:
            self.client.info()
            logging.info("Connected to Opensearch Database successfully!")
        except Exception as err:
            logging.error("Failed to connect to opensearch: ", err)

    def ingest_document(self, index: str, document: dict, id: str = None):
        """
        Ingests a document into the database
        """
        response = self.client.index(index=index, body=document, id=id, refresh=True)
        return response
