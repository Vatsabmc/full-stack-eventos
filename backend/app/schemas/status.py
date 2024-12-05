import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class StatusBase(SQLModel):
    status: str = Field(unique=True, min_length=1, max_length=50)


# Properties to receive on event creation
class StatusCreate(StatusBase):
    pass


# Properties to receive on status update
class StatusUpdate(StatusBase):
    pass


# Properties to return via API, id is always required
class StatusPublic(StatusBase):
    id: uuid.UUID


class StatusesPublic(SQLModel):
    data: list[StatusPublic]
    count: int
