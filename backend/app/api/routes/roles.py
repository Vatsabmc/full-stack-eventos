import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Role
from app.schemas.roles import RoleCreate, RolePublic, RolesPublic

router = APIRouter(prefix="/roles", tags=["users"])


@router.get("/", response_model=RolesPublic)
def read_roles(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve roles.
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


@router.get("/{id}", response_model=RolePublic)
def read_role(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get role by ID.
    """
    role = session.get(Role, id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return role


@router.post("/", response_model=RolePublic)
def create_role(
    *, session: SessionDep, current_user: CurrentUser, role_in: RoleCreate
) -> Any:
    """
    Create new role.
    """
    if current_user.is_superuser:
        role = Role.model_validate(role_in)
        session.add(role)
        session.commit()
        session.refresh(role)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return role
