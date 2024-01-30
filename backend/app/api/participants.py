from http import HTTPStatus

from app.application.services import ParticipantService
from app.core.exceptions import (
    MeetingClosed,
    ObjectIsNoneException,
    UserAlreadyExists,
)
from app.domain.schemas import (
    GetParticipant,
    ParticipantCreate,
    ParticipantUpdate,
)
from fastapi import APIRouter, HTTPException

from .dependencies import UoWDep


router = APIRouter(prefix="/participants", tags=["participants"])


@router.get(
    "/",
    response_model=list[GetParticipant],
    summary="Получить список участников.",
)
async def get_users(uow: UoWDep):
    """Получить список пользователей."""
    return await ParticipantService().get_users(uow)


@router.get(
    "/{id}", response_model=GetParticipant, summary="Получить участника по id."
)
async def get_user(id: int, uow: UoWDep):
    try:
        return await ParticipantService().get_user(uow, id)
    except AttributeError:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Пользователь с id = {id} отсутствует.",
        )


@router.post("/", response_model=GetParticipant, summary="Создать участника.")
async def create_user(user: ParticipantCreate, uow: UoWDep):
    """Создать пользователя."""
    try:
        return await ParticipantService().create_user(uow, user)
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Запись на собрание уже закрыта.",
        )
    except (ObjectIsNoneException, UserAlreadyExists) as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )


@router.patch(
    "/{id}", response_model=GetParticipant, summary="Обновить пользователя."
)
async def update_user(user: ParticipantUpdate, uow: UoWDep, id: int):
    """Редавктировать инфо о пользователе."""
    try:
        return await ParticipantService().update_user(uow, id, user)
    except (UserAlreadyExists, ObjectIsNoneException) as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Запись на собрание уже закрыта.",
        )


@router.delete(
    "/{id}", response_model=GetParticipant, summary="Удалить пользователя."
)
async def delete_user(uow: UoWDep, id: int):
    """Удалить пользователя."""
    try:
        return await ParticipantService().delete_user(uow, id)
    except ObjectIsNoneException as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(error),
        )
