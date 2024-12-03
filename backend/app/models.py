import uuid

from sqlmodel import Field, Relationship
from app.schemas.users import UserBase
from app.schemas.events import EventBase


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    events: list["Event"] = Relationship(back_populates="owner",
                                         cascade_delete=True)


# Database model, database table inferred from class name
class Event(EventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="events")
