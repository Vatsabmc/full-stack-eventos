import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Category
from app.schemas.categories import CategoryCreate, CategoryPublic, CategoriesPublic

router = APIRouter(prefix="/event_categories", tags=["events|categories"])


@router.get("/", response_model=CategoriesPublic,
            summary="Lista todos las categorias de eventos",
            response_description="Lista de todas las categorias de eventos creados")
def read_categories(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 10
) -> Any:
    """
    Lista todos las categorias de eventos existentes.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Category)
        count = session.exec(count_statement).one()
        statement = select(Category).offset(skip).limit(limit)
        categories = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Category)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Category)
            .offset(skip)
            .limit(limit)
        )
        categories = session.exec(statement).all()

    return CategoriesPublic(data=categories, count=count)


@router.get("/{id}", response_model=CategoryPublic,
            summary="Lista una categoria de evento por id",
            response_description="Categoria de evento filtrado por id")
def read_category(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Devuelve la categoria de evento asociado al id.
    """
    status = session.get(Category, id)
    if not status:
        raise HTTPException(status_code=404, detail="Category not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status


@router.post("/", response_model=CategoryPublic,
             summary="Crea una nueva categoria de evento",
             response_description="Id de la nueva categoria creado.")
def create_category(
    *, session: SessionDep, current_user: CurrentUser, status_in: CategoryCreate
) -> Any:
    """
    Crea una nueva categoria de evento con la información:
    - **category**: nombre de la nueva categoria. Debe ser unica
    """
    if current_user.is_superuser:
        status = Category.model_validate(status_in)
        session.add(status)
        session.commit()
        session.refresh(status)
    else:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return status
