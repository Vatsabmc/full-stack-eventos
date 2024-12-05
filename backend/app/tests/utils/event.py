from sqlmodel import Session

from app import crud
from app.models import Event
from app.schemas.events import EventCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_event(db: Session) -> Event:
    user = create_random_user(db)
    organizer_id = user.id
    assert organizer_id is not None
    title = random_lower_string()
    description = random_lower_string()
    event_in = EventCreate(title=title, description=description)
    return crud.create_event(session=db, event_in=event_in, organizer_id=organizer_id)
