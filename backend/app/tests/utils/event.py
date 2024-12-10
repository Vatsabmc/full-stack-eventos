from sqlmodel import Session

from app import crud
from app.models import Event
from app.schemas.events import EventCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.role import create_random_role
from app.tests.utils.status import create_random_status
from app.tests.utils.category import create_random_category
from app.tests.utils.utils import random_lower_string, random_dates


def create_random_event(db: Session) -> Event:
    user = create_random_user(db)
    organizer_id = user.id
    assert organizer_id is not None

    status = create_random_status(db)
    status_id = status.id
    assert status_id is not None

    category = create_random_category(db)
    category_id = category.id
    assert category_id is not None

    title = random_lower_string()
    description = random_lower_string()
    start_datetime, end_datetime = random_dates()
    location = random_lower_string()
    event_in = EventCreate(title=title, description=description,
                           start_datetime=start_datetime,
                           end_datetime=end_datetime, location=location,
                           capacity=100)
    return crud.create_event(session=db, event_in=event_in,
                             organizer_id=organizer_id, status_id=status_id,
                             category_id=category_id)
