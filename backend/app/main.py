import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


description = """
Mis Eventos permite administrar el ciclo de vida de un evento, desde su creación y configuración hasta la gestión de asistentes. 🚀
"""
tags_metadata = [
    {
        "name": "login",
        "description": "Operaciones de autenticación de usuarios",
    },
    {
        "name": "users",
        "description": "Operaciones con usuarios.",
    },
    {
        "name": "events",
        "description": "Operaciones con eventos. Adicionalmente, permite añadir usuarios (asistentes) a eventos.",
    },
    {
        "name": "events|sessions",
        "description": "Operaciones con sesiones. Adicionalmente, permite añadir usuarios (asistentes) a sesiones.",
    },
    {
        "name": "utils",
        "description": "Operaciones de utilidades para probar el backend.",
    },
    {
        "name": "private",
        "description": "Creación de usuarios en ambiente local.",
    },
]


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
