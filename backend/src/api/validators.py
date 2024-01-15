import contextlib
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException

from src.containers import Container
from src.core.exceptions import ObjectIsNoneException
from src.domain.models import User


@inject
async def validate_user_exists(
    user: User, user_repository=Depends(Provide[Container.user_repository])
):
    """Если пользователь существует - ошибка 400."""
    with contextlib.suppress(ObjectIsNoneException):
        exists_user = await user_repository.get_by_attributes(
            name=user.name, phone=user.phone, email=user.email
        )
        if exists_user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Пользователь с такими параметрами уже существует!",
            )
