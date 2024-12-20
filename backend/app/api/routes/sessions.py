import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import Sessions, Event
from app.schemas.sessions import (
    SessionsCreate, SessionsPublic, SessionssPublic, SessionsUpdate)
from app.schemas.utils import Message

router = APIRouter(prefix="/sessions", tags=["events|sessions"])


@router.get("/", response_model=SessionssPublic,
            summary="Lista todos las sesiones",
            response_description="Lista de todas las sesiones creadas")
def read_sessionss(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Lista todas las sesiones
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Sessions)
        count = session.exec(count_statement).one()
        statement = select(Sessions).offset(skip).limit(limit)
        sessions = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Sessions)
            .where(Sessions.organizer_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Sessions)
            .where(Sessions.organizer_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        sessions = session.exec(statement).all()

    return SessionssPublic(data=sessions, count=count)


@router.get("/{sessions_id}", response_model=SessionsPublic)
def read_sessions(session: SessionDep, current_user: CurrentUser, sessions_id: uuid.UUID) -> Any:
    """
    Get sessions by ID.
    """
    db_sessions = session.get(Sessions, sessions_id)
    if not db_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    db_event = session.get(Event, db_sessions.event_id)
    if not current_user.is_superuser or (db_event.organizer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return db_sessions


@router.post("/", response_model=SessionsPublic,
    summary="Crea sesiones",
    response_description="Id de la nueva sesión creada y id del evento")
def create_sessions(
    *, session: SessionDep, current_user: CurrentUser, sessions_in: SessionsCreate
) -> Any:
    """
    Crea una nueva sesión con la información:
    - **title**: requerido
    - **description**: opcional
    - **start_datetime: requerido. Formato YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][[±]HH[:]MM]
    - **end_datetime: requerido. Formato YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][[±]HH[:]MM]
    - **capacity: requerido
    - **event_id**: requerido
    """
    db_event = session.get(Event, sessions_in.event_id)
    if not current_user.is_superuser or (db_event.organizer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions to create a session for this event.")

    sessions = Sessions.model_validate(sessions_in)
    session.add(sessions)
    session.commit()
    session.refresh(sessions)
    return sessions


@router.patch('/{event_id}', response_model=SessionsPublic,
    summary="Actualiza los campos enviados de una sesión por id",
    response_description="Id de la sesión modificado")
def update_sessions(session: SessionDep, current_user: CurrentUser,
                    sessions_id: uuid.UUID, sessions_in: SessionsUpdate) -> Any:
    """
    Actualiza una sesión con la nueva información enviada.
    """

    db_sessions = session.get(Sessions, sessions_id)
    if not db_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    db_event = session.get(Event, db_sessions.event_id)
    if not current_user.is_superuser or (db_event.organizer_id != current_user.id):
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    db_sessions = crud.update_session(session=session, db_sessions=db_sessions, sessions_in=sessions_in)
    return db_event


@router.delete("/{sessions_id}",
    summary="Elimina una sesión por id")
def delete_sessions(
    session: SessionDep, current_user: CurrentUser, sessions_id: uuid.UUID
) -> Message:
    """
    Elimina una sesión
    """
    db_sessions = session.get(Sessions, sessions_id)
    if not db_sessions:
        raise HTTPException(status_code=404, detail="Sessions not found")

    db_event = session.get(Event, db_sessions.event_id)
    if not current_user.is_superuser or (db_event.organizer_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    session.delete(db_sessions)
    session.commit()
    return Message(message="Session deleted successfully")


@router.post('/attend/{sessions_id}')
async def add_user_to_event(session: SessionDep, current_user: CurrentUser, sessions_id: uuid.UUID):
    """
    Asigna al usuario actual a la sesión especificado a través del event_id.
    """
    db_sessions = session.get(Sessions, sessions_id)
    db_sessions.attendees.append(current_user)

    db_sessions = crud.add_attendee_sessions(session=session, db_sessions=db_sessions)
    return db_sessions
