import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Status
from app.schemas.status import StatusCreate, StatusPublic, StatusesPublic

router = APIRouter(prefix="/event_status", tags=["events|status"])


@router.get("/", response_model=StatusesPublic,
    summary="Lista todos los estados de eventos",
    response_description="Lista de todo los estados de eventos creados")
def read_statuses(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10
) -> Any:
    """
    Lista todos los estados de eventos existentes.
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


@router.get("/{id}", response_model=StatusPublic,
    summary="Lista un estado de evento por id",
    response_description="Estado de evento filtrado por id")
def read_status(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Devuelve el estado de evento asociado al id.
    """
    status = session.get(Status, id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status


@router.post("/", response_model=StatusPublic,
    summary="Crea un nuevo estado de evento",
    response_description="Id del nuevo estado creado.")
def create_status(
    *, session: SessionDep, current_user: CurrentUser, status_in: StatusCreate
) -> Any:
    """
    Crea un nuevo estado de evento con la información:
    - **status**: nombre del estado. Debe ser unico
    """
    if current_user.is_superuser:
        status = Status.model_validate(status_in)
        session.add(status)
        session.commit()
        session.refresh(status)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status
