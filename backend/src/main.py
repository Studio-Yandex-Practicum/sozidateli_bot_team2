from fastapi import FastAPI

from src.api import routers
from src.core import Settings


def create_app() -> FastAPI:
    """Фабрика FastAPI."""

    app = FastAPI(title=Settings.app_title)

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
