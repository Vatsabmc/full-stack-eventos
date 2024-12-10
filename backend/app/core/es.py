from elasticsearch import Elasticsearch

from app.core.config import settings


class ES_connector:
    def __init__(self) -> None:
        self.es_client = None
        self.connect()

    def connect(self):
        es = Elasticsearch(
            hosts=[f"http://{settings.ES_SERVER}:{settings.ES_PORT}"],
            basic_auth=(settings.ES_USER, settings.ES_PASSWORD),
            verify_certs=False)
        self.es_client = es

    def create_index(self, index_name):
        self.es_client.indices.delete(index=index_name, ignore_unavailable=True)
        self.es_client.indices.create(index=index_name)

    def insert_documents(self, index_name, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': index_name}})
            operations.append(document)
        return self.es_client.bulk(operations=operations)

    def insert_document(self, index_name, document_type, document_id, document):
        try:
            return self.es_client.index(index=index_name, doc_type=document_type,
                                        id=document_id, body=document,
                                        refresh='wait_for', request_timeout=30)
        except Exception as e:
            print(e)

    def search(self, index_name, **query_args):
        return self.es_client.search(index=index_name, **query_args)

    def get_data(self, index_name, search_query, size=10):
        try:
            result = self.es_client.search(index=index_name, body=search_query,
                                           allow_partial_search_results=True,
                                           size=size, request_timeout=120)
            return result
        except Exception as e:
            print(e)

    def retrieve_document(self, index_name, id):
        return self.es.get(index=index_name, id=id)
