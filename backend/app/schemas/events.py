import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import field_validator, ValidationInfo, FutureDatetime


# Shared properties
class EventBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on event creation
class EventCreate(EventBase):
    start_datetime: FutureDatetime
    end_datetime: FutureDatetime
    location: str = Field(max_length=255)
    capacity: int = Field(gt=5)
    attendee_count: int = Field(default=0, ge=0)
    organizer_id: uuid.UUID
    status_id: uuid.UUID    
    category_id: uuid.UUID

    @field_validator("end_datetime")
    @classmethod
    def validate_end_date(cls, value: datetime, info: ValidationInfo) -> datetime:

        # Check if end_datetime is less than or equal to start_datetime
        if "start_datetime" in info.data and value <= info.data["start_datetime"]:
            # Raise a ValueError with the error message
            raise ValueError("La fecha de finalización debe ser mayor a la de inicio.")

        # Return the value if it passes validation
        return value


# Properties to receive on event update
class EventUpdate(EventBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    description: str | None = Field(default=None, max_length=255)
    start_datetime: datetime | None
    end_datetime: datetime | None
    location: str | None = Field(max_length=255)
    capacity: int | None = Field(gt=5)
    attendee_count: int | None = Field(ge=0)
    organizer_id: uuid.UUID | None
    status_id: uuid.UUID | None
    category_id: uuid.UUID | None


# Properties to return via API, id is always required
class EventPublic(EventBase):
    id: uuid.UUID
    organizer_id: uuid.UUID


class EventsPublic(SQLModel):
    data: list[EventPublic]
    count: int
