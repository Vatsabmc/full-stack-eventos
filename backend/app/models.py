import uuid

from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Column, DateTime
from app.schemas.users import UserBase
from app.schemas.events import EventBase
from app.schemas.roles import RoleBase
from app.schemas.status import StatusBase
from app.schemas.sessions import SessionsBase
from app.schemas.categories import CategoryBase


class EventAttendeeLink(SQLModel, table=True):
    event_id: uuid.UUID = Field(
        foreign_key="event.id", nullable=False, primary_key=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, primary_key=True
    )


class SessionAttendeeLink(SQLModel, table=True):
    session_id: uuid.UUID = Field(
        foreign_key="sessions.id", nullable=False, primary_key=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, primary_key=True
    )


class Role(RoleBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    role: str = Field(unique=True, max_length=25)

    # Establish a one-to-many relationship
    user: list["User"] = Relationship(back_populates="role")


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    role_id: uuid.UUID = Field(foreign_key="role.id")

    # Establish the back references
    role: Role = Relationship(back_populates="user")

    # Establish a one-to-many relationship
    organizer_of: list["Event"] = Relationship(back_populates="organizer")
    speaker_of: list["Sessions"] = Relationship(back_populates="speaker")

    # Establish a many-to-many relationship
    events: list["Event"] = Relationship(back_populates="attendees", link_model=EventAttendeeLink)
    sessions: list["Sessions"] = Relationship(back_populates="attendees", link_model=SessionAttendeeLink)


class Status(StatusBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(unique=True, max_length=25)

    # Establish a one-to-many relationship
    event: list["Event"] = Relationship(back_populates="status")


class Category(CategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category: str = Field(unique=True, max_length=25)

    # Establish a one-to-many relationship
    event: list["Event"] = Relationship(back_populates="category")


# Database model, database table inferred from class name
class Event(EventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)
    start_datetime: datetime = Column(DateTime(timezone=True), nullable=False)
    end_datetime: datetime = Column(DateTime(timezone=True), nullable=False)
    location: str = Field(max_length=255)
    capacity: int = Field(nullable=False)
    attendee_count: int = Field(nullable=False)
    organizer_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    category_id: uuid.UUID = Field(foreign_key="category.id", nullable=False)
    status_id: uuid.UUID = Field(foreign_key="status.id", nullable=False)

    # Establish the back references
    organizer: User = Relationship(back_populates="organizer_of")
    status: Status = Relationship(back_populates="event")
    category: Category = Relationship(back_populates="event")

    # Establish a one-to-many relationship
    sessions: list["Sessions"] = Relationship(back_populates="event")

    # Establish a many-to-many relationship
    attendees: list["User"] = Relationship(back_populates="events", link_model=EventAttendeeLink)


class Sessions(SessionsBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str = Field(max_length=255)
    start_datetime: datetime = Column(DateTime(timezone=True),nullable=False)
    end_datetime: datetime = Column(DateTime(timezone=True),nullable=False)
    capacity: int = Field(nullable=False)
    attendee_count: int = Field(nullable=False)
    event_id: uuid.UUID = Field(foreign_key="event.id", nullable=False, ondelete="CASCADE")
    speaker_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    # Establish the back references
    event: Event = Relationship(back_populates="sessions")
    speaker: User = Relationship(back_populates="speaker_of")

    # Establish a many-to-many relationship
    attendees: list["User"] = Relationship(back_populates="sessions", link_model=SessionAttendeeLink)
