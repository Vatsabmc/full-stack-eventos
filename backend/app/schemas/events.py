import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class EventBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on event creation
class EventCreate(EventBase):
    pass


# Properties to receive on event update
class EventUpdate(EventBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Properties to return via API, id is always required
class EventPublic(EventBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class EventsPublic(SQLModel):
    data: list[EventPublic]
    count: int


