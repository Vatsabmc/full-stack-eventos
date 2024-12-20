from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, Role, Status, Category
from app.schemas.users import UserCreate
from app.schemas.roles import RoleCreate
from app.schemas.status import StatusCreate
from app.schemas.categories import CategoryCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    # Roles por usuario
    role = session.exec(
        select(Role).where(Role.role == settings.ROLES[0])
    ).first()
    if not role:
        print(settings.ROLES[0])
        for preset in settings.ROLES:
            role_in = RoleCreate(
                role=preset
            )
            role = crud.create_role(session=session, role_create=role_in)
            if preset == settings.ROLES[0]:
                role_admin = role

    # Estados de evento iniciales
    status = session.exec(
        select(Status).where(Status.status == settings.STATUSES[0])
    ).first()
    if not status:
        for preset in settings.STATUSES:
            status_in = StatusCreate(
                status=preset
            )
            status = crud.create_status(session=session, status_create=status_in)

    # Categorias de evento iniciales
    category = session.exec(
        select(Category).where(Category.category == settings.CATEGORIES[0])
    ).first()
    if not category:
        for preset in settings.CATEGORIES:
            category_in = CategoryCreate(
                category=preset
            )
            category = crud.create_category(session=session, category_create=category_in)

    # Crear primer super usuario
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True
        )
        user = crud.create_user(session=session, user_create=user_in, role_id=role_admin.id)
