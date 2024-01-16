from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from src.api.validators import validate_user_exists
from src.application.repositories import BaseRepository
from src.containers import Container
from src.core.exceptions import ObjectAlreadyExists
from src.domain.schemas import UserCreate, UserDB


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/", response_model=list[UserDB], summary="Получить список пользователей."
)
@inject
async def get_users(
    user_repository: BaseRepository = Depends(
        Provide[Container.user_repository]
    ),
):
    """Получить список пользователей."""
    return await user_repository.get_list()


@router.post("/", response_model=UserDB, summary="Создать пользователя.")
@inject
async def create_user(
    user: UserCreate,
    user_repository: BaseRepository = Depends(
        Provide[Container.user_repository]
    ),
):
    """Создать пользователя."""
    try:
        await validate_user_exists(user)
    except ObjectAlreadyExists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Пользователь с такими параметрами уже существует!",
        )
    new_user = await user_repository.create(user)
    return new_user
