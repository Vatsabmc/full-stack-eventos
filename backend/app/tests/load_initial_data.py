import json
import logging
from app.core.es import ES_connector
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

es = ES_connector()


def load_data() -> None:
    es.create_index(index_name=settings.ES_INDEX)
    logger.info("Loading dummy data data")
    with open('/app/app/tests/data.json', 'rt') as f:
        documents = json.loads(f.read())
    es.insert_documents(index_name=settings.ES_INDEX,
                        documents=documents)
    logger.info("Dummy data created")
