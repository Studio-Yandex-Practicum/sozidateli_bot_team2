import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core import settings
from app.infrastructure.db import async_session_maker
from .users import get_user_db, get_user_manager
from app.domain.schemas import UserCreate


async def get_async_session():
    async with async_session_maker() as async_session:
        yield async_session


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr, password: str, is_superuser: bool = False
):
    async with get_async_session_context() as session, get_user_db_context(
        session
    ) as user_db, get_user_manager_context(user_db) as user_manager:
        with contextlib.suppress(UserAlreadyExists):
            await user_manager.create(
                UserCreate(
                    email=email,
                    password=password,
                    is_superuser=is_superuser,
                )
            )


async def create_first_superuser():
    if (
        settings.first_superuser_email is not None and
        settings.first_superuser_password is not None
    ):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
