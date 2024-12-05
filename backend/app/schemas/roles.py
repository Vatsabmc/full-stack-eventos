import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class RoleBase(SQLModel):
    role: str = Field(unique=True, min_length=1, max_length=50)


# Properties to receive on event creation
class RoleCreate(RoleBase):
    pass


# Properties to receive on role update
class RoleUpdate(RoleBase):
    pass


# Properties to return via API, id is always required
class RolePublic(RoleBase):
    id: uuid.UUID


class RolesPublic(SQLModel):
    data: list[RolePublic]
    count: int
