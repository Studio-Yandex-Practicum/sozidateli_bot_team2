from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.validators import validate_user_exists
from src.application.repositories import BaseRepository
from src.containers import Container
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
    await validate_user_exists(user)
    new_user = await user_repository.create(user)
    return new_user
