import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Status
from app.schemas.status import StatusCreate, StatusPublic, StatusesPublic

router = APIRouter(prefix="/event_status", tags=["events"])


@router.get("/", response_model=StatusesPublic)
def read_statuses(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve statuses.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Status)
        count = session.exec(count_statement).one()
        statement = select(Status).offset(skip).limit(limit)
        statuses = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Status)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Status)
            .offset(skip)
            .limit(limit)
        )
        statuses = session.exec(statement).all()

    return StatusesPublic(data=statuses, count=count)


@router.get("/{id}", response_model=StatusPublic)
def read_status(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get status by ID.
    """
    status = session.get(Status, id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status


@router.post("/", response_model=StatusPublic)
def create_status(
    *, session: SessionDep, current_user: CurrentUser, status_in: StatusCreate
) -> Any:
    """
    Create new status.
    """
    if current_user.is_superuser:
        status = Status.model_validate(status_in)
        session.add(status)
        session.commit()
        session.refresh(status)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status
