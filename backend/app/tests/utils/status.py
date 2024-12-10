from sqlmodel import Session

from app import crud
from app.models import Status
from app.schemas.status import StatusCreate
from app.tests.utils.utils import random_lower_string


def create_random_status(db: Session) -> Status:
    status = random_lower_string()
    status_in = StatusCreate(status=status)
    return crud.create_status(session=db, status_create=status_in)
