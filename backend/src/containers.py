from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.application.repositories.base import BaseRepository
from src.core.settings import Settings
from src.domain.models import Meeting, User


class Container(containers.DeclarativeContainer):
    """Dependency Injector Container."""

    wiring_config = containers.WiringConfiguration(
        modules=["src.api.users", "src.api.meetings", "src.api.validators"],
    )

    async_engine = providers.Singleton(create_async_engine, Settings.db_url)

    db_session_factory = providers.Factory(AsyncSession, bind=async_engine)

    user_repository = providers.Factory(
        BaseRepository,
        model=User,
        session_factory=db_session_factory,
    )

    meeting_repository = providers.Factory(
        BaseRepository,
        model=Meeting,
        session_factory=db_session_factory,
    )
