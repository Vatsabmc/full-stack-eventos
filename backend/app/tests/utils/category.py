from sqlmodel import Session

from app import crud
from app.models import Category
from app.schemas.categories import CategoryCreate
from app.tests.utils.utils import random_lower_string


def create_random_category(db: Session) -> Category:
    category = random_lower_string()
    category_in = CategoryCreate(category=category)
    return crud.create_category(session=db, category_create=category_in)
