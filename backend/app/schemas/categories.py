import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class CategoryBase(SQLModel):
    category: str = Field(unique=True, min_length=1, max_length=50)


# Properties to receive on event creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive on status update
class CategoryUpdate(CategoryBase):
    pass


# Properties to return via API, id is always required
class CategoryPublic(CategoryBase):
    id: uuid.UUID


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int
