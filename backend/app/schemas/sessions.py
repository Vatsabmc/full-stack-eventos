import uuid

from datetime import datetime
from sqlmodel import Field, SQLModel
from pydantic import field_validator, ValidationInfo, FutureDatetime


# Shared properties
class SessionsBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on session creation
class SessionsCreate(SessionsBase):
    start_datetime: FutureDatetime
    end_datetime: FutureDatetime
    capacity: int = Field(gt=5)
    attendee_count: int = Field(default=0, ge=0)
    event_id: uuid.UUID
    speaker_id: uuid.UUID | None = Field(default=None)

    @field_validator("end_datetime")
    @classmethod
    def validate_end_date(cls, value: datetime, info: ValidationInfo) -> datetime:

        # Check if end_datetime is less than or equal to start_datetime
        if "start_datetime" in info.data and value <= info.data["start_datetime"]:
            # Raise a ValueError with the error message
            raise ValueError("La fecha de finalización debe ser mayor a la de inicio.")

        # Return the value if it passes validation
        return value


# Properties to receive on session update
class SessionsUpdate(SessionsBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore
    description: str | None = Field(default=None, max_length=255)
    start_datetime: datetime | None
    end_datetime: datetime | None
    capacity: int | None = Field(gt=5)
    attendee_count: int | None = Field(ge=0)
    event_id: uuid.UUID | None
    speaker_id: uuid.UUID | None


# Properties to return via API, id is always required
class SessionsPublic(SessionsBase):
    id: uuid.UUID
    event_id: uuid.UUID
    speaker_id: uuid.UUID


class SessionssPublic(SQLModel):
    data: list[SessionsPublic]
    count: int


class SessionsAttendeePublic(SessionsBase):
    id: uuid.UUID
    event_id: uuid.UUID
    speaker_id: uuid.UUID
