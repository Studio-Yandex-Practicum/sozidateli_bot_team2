from fastapi import FastAPI

from src.api import routers
from src.core import Settings
from src.infrastructure.admin import admin


def create_app() -> FastAPI:
    """Фабрика FastAPI."""

    app = FastAPI(title=Settings.app_title)
    admin.mount_to(app)

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
