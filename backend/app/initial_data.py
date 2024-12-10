import logging

from sqlmodel import Session

from app.core.db import engine, init_db
from app.core.config import settings
from app.tests.load_initial_data import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")
    if settings.ENVIRONMENT == "local":
        load_data()


if __name__ == "__main__":
    main()
