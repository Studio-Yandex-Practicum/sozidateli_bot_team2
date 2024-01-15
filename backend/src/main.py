from fastapi import FastAPI

from src.api import routers
from src.core import Settings

from .containers import Container


def create_app() -> FastAPI:
    """Фабрика FastAPI."""

    container = Container()
    app = FastAPI(title=Settings.app_title)
    app.container = container

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
