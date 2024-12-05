import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import Event
from app.schemas.events import EventCreate, EventPublic, EventsPublic, EventUpdate
from app.schemas.utils import Message

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=EventsPublic)
def read_events(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve events.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Event)
        count = session.exec(count_statement).one()
        statement = select(Event).offset(skip).limit(limit)
        events = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Event)
            .where(Event.organizer_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Event)
            .where(Event.organizer_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        events = session.exec(statement).all()

    return EventsPublic(data=events, count=count)


@router.get("/{event_id}", response_model=EventPublic)
def read_event(session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID) -> Any:
    """
    Get event by ID.
    """
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not current_user.is_superuser and (event.organizer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return event


@router.post("/", response_model=EventPublic)
def create_event(
    *, session: SessionDep, current_user: CurrentUser, event_in: EventCreate
) -> Any:
    """
    Create new event.
    """
    event = Event.model_validate(event_in, update={"organizer_id": current_user.id})
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.patch('/{event_id}', response_model=EventPublic)
def update_event(session: SessionDep, current_user: CurrentUser,
                 event_id: uuid.UUID, event_in: EventUpdate) -> Any:

    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not current_user.is_superuser or (db_event.organizer_id != current_user.id):
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    db_event = crud.update_event(session=session, db_event=db_event, event_in=event_in)
    return db_event


@router.delete("/{event_id}")
def delete_event(
    session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID
) -> Message:
    """
    Delete an event.
    """
    db_event = session.get(Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not current_user.is_superuser and (db_event.organizer_id != current_user.id):
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    session.delete(db_event)
    session.commit()
    return Message(message="Event deleted successfully")


@router.post('/attend/{event_id}')
async def add_user_to_event(session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID):
    db_event = session.get(Event, event_id)
    db_event.attendees.append(current_user)

    db_event = crud.add_attendee_event(session=session, db_event=db_event)
    return db_event
