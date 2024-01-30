from fastapi import FastAPI, Request

from app.api import routers
from app.core import Settings
from app.infrastructure.admin import admin


def create_app() -> FastAPI:
    """Фабрика FastAPI."""

    app = FastAPI(title=Settings.app_title)
    admin.mount_to(app)

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
