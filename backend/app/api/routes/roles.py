import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Role
from app.schemas.roles import RoleCreate, RolePublic, RolesPublic

router = APIRouter(prefix="/roles", tags=["users"])


@router.get("/", response_model=RolesPublic,
    summary="Lista todos los roles",
    response_description="Lista de todo los roles creados")
def read_roles(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10
) -> Any:
    """
    Lista todos los roles existentes.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Role)
        count = session.exec(count_statement).one()
        statement = select(Role).offset(skip).limit(limit)
        roles = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Role)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Role)
            .offset(skip)
            .limit(limit)
        )
        roles = session.exec(statement).all()

    return RolesPublic(data=roles, count=count)


@router.get("/{id}", response_model=RolePublic,
    summary="Lista un rol por id",
    response_description="Rol filtrado por id")
def read_role(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Devuelve el rol asociado al id.
    """
    role = session.get(Role, id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return role


@router.post("/", response_model=RolePublic,
    summary="Crea un nuevo rol",
    response_description="Id del nuevo rol creado.")
def create_role(
    *, session: SessionDep, current_user: CurrentUser, role_in: RoleCreate
) -> Any:
    """
    Crea un nuevo rol con la información:
    - **role**: nombre del rol. Debe ser unico
    """
    if current_user.is_superuser:
        role = Role.model_validate(role_in)
        session.add(role)
        session.commit()
        session.refresh(role)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return role
