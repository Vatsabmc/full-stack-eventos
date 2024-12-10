import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, Event, Role, Status, Category, Sessions
from app.schemas.users import UserCreate, UserUpdate
from app.schemas.roles import RoleCreate
from app.schemas.events import EventCreate, EventUpdate
from app.schemas.sessions import SessionsCreate, SessionsUpdate
from app.schemas.status import StatusCreate
from app.schemas.categories import CategoryCreate


# C roles
def create_role(*, session: Session, role_create: RoleCreate) -> Role:
    db_obj = Role(role=role_create.role)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


# C status
def create_status(*, session: Session, status_create: StatusCreate) -> Status:
    db_obj = Status(status=status_create.status)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


# C category
def create_category(*, session: Session, category_create: CategoryCreate) -> Category:
    db_obj = Category(category=category_create.category)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


# CRUD users
def create_user(*, session: Session, user_create: UserCreate, role_id: uuid.UUID) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password),
                             "role_id": role_id}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# CRUD events
def create_event(*, session: Session, event_in: EventCreate,
                 organizer_id: uuid.UUID, status_id: uuid.UUID,
                 category_id: uuid.UUID) -> Event:
    db_event = Event.model_validate(event_in, update={"organizer_id": organizer_id,
                                                      "status_id": status_id,
                                                      "category_id": category_id})
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


def update_event(*, session: Session, db_event: Event, event_in: EventUpdate) -> Any:
    event_data = event_in.model_dump(exclude_unset=True)
    db_event.sqlmodel_update(event_data)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


def add_attendee_event(*, session: Session, db_event: Event) -> Event:
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


# CRUD sessions
def create_sessions(*, session: Session, sessions_in: SessionsCreate, event_id: uuid.UUID) -> Sessions:
    db_sessions = Event.model_validate(sessions_in, update={"event_id": event_id})
    session.add(db_sessions)
    session.commit()
    session.refresh(db_sessions)
    return db_sessions


def update_sessions(*, session: Session, db_sessions: Sessions, sessions_in: SessionsUpdate) -> Any:
    event_data = sessions_in.model_dump(exclude_unset=True)
    db_sessions.sqlmodel_update(event_data)
    session.add(db_sessions)
    session.commit()
    session.refresh(db_sessions)
    return db_sessions


def add_attendee_sessions(*, session: Session, db_sessions: Sessions) -> Sessions:
    session.add(db_sessions)
    session.commit()
    session.refresh(db_sessions)
    return db_sessions
