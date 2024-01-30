from contextlib import asynccontextmanager
from app.api import routers
from app.core import Settings
from app.infrastructure.admin import admin
from app.core.init_db import create_first_superuser
from fastapi import FastAPI


@asynccontextmanager
async def on_startup(app: FastAPI):
    await create_first_superuser()
    yield


def create_app() -> FastAPI:
    """Фабрика FastAPI."""

    app = FastAPI(title=Settings.app_title, lifespan=on_startup)
    admin.mount_to(app)

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
