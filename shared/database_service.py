from opensearchpy import OpenSearch, NotFoundError

from shared.logging_helper import logger


class DatabaseService:
    def __init__(self, host: str, username: str, password: str):
        auth = (username, password)
        self.client = OpenSearch(
            hosts=[host],
            http_auth=auth,
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
        )

        try:
            self.client.info()
            logger.info("Connected to Opensearch Database successfully!")
        except Exception as err:
            logger.exception("Failed to connect to opensearch: ", err)

    def __clean_opensearch_response(self, opensearch_response: dict) -> None:
        """
        Cleans each opensearch hit object and return the intended resource document
        """
        result = []

        for hit in opensearch_response["hits"]["hits"]:
            temp = hit["_source"]
            temp["_id"] = hit["_id"]
            result.append(temp)

        return result

    def ingest_document(self, index: str, document: dict, id: str = None):
        """
        Ingests a document into the database
        """
        response = self.client.index(index=index, body=document, id=id, refresh=True)
        return response

    def fetch_documents(self, index: str, query_body: dict) -> dict:
        """
        Retrieves documents from the database based on the query body
        """
        response = self.client.search(index=index, body=query_body)
        return self.__clean_opensearch_response(response)

    def update_document(
        self, index: str, document_id: str, updated_fields: dict
    ) -> None:
        """
        Partially updates a document in the database
        """
        update_body = {"doc": updated_fields}

        self.client.update(index=index, id=document_id, body=update_body)

    def fetch_document_by_id(self, index: str, document_id: str) -> dict | None:
        """
        fetch a document by ID. Returns null if the resource is not found
        """
        try:
            # Attempt to get the document
            response = self.client.get(index=index, id=document_id)
            document = response.get("_source", {})

            return document
        except NotFoundError:
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
