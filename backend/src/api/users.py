from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.application.services import UserService
from src.core.exceptions import (
    MeetingClosed,
    ObjectAlreadyExists,
    ObjectIsNoneException,
)
from src.domain.schemas import GetUser, UserCreate, UserUpdate

from .dependencies import UoWDep


router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/", response_model=list[GetUser], summary="Получить список пользователей."
)
async def get_users(uow: UoWDep):
    """Получить список пользователей."""
    return await UserService().get_users(uow)


@router.post("/", response_model=GetUser, summary="Создать пользователя.")
async def create_user(user: UserCreate, uow: UoWDep):
    """Создать пользователя."""
    try:
        return await UserService().create_user(uow, user)
    except ObjectAlreadyExists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Пользователь с такими параметрами уже существует!",
        )
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Запись на собрание уже закрыта.",
        )
    except ObjectIsNoneException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Собрания с таким id не существует.",
        )


@router.patch(
    "/{id}", response_model=GetUser, summary="Обновить пользователя."
)
async def update_user(user: UserUpdate, uow: UoWDep, id: int):
    """Редавктировать инфо о пользователе."""
    try:
        return await UserService().update_user(uow, id, user)
    except ObjectAlreadyExists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Пользователь с такими параметрами уже существует!",
        )
    except ObjectIsNoneException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Собрания с таким id не существует.",
        )
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Запись на собрание уже закрыта.",
        )


@router.delete(
    "/{id}", response_model=GetUser, summary="Удалить пользователя."
)
async def delete_user(uow: UoWDep, id: int):
    """Удалить пользователя."""
    try:
        return await UserService().delete_user(uow, id)
    except ObjectIsNoneException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Пользователя с таким id не существует!",
        )
