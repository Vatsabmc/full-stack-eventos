from sqlmodel import Session

from app import crud
from app.models import Role
from app.schemas.roles import RoleCreate
from app.tests.utils.utils import random_lower_string


def create_random_role(db: Session) -> Role:
    role = random_lower_string()
    role_in = RoleCreate(role=role)
    return crud.create_role(session=db, role_create=role_in)
