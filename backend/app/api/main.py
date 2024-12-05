from fastapi import APIRouter

from app.api.routes import (
    login,
    private,
    users,
    roles,
    utils,
    events,
    status,
    sessions
    )
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(roles.router)
api_router.include_router(users.router)
api_router.include_router(status.router)
api_router.include_router(events.router)
api_router.include_router(sessions.router)
api_router.include_router(utils.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
