from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.application.services import MeetingServices
from src.core.exceptions import (
    InvalidDate,
    MeetingClosed,
    ObjectIsNoneException,
)
from src.domain.schemas import (
    GetMeeting,
    MeetingCreate,
    MeetingParticipants,
    MeetingUpdate,
)

from .dependencies import UoWDep


router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get(
    "/", response_model=list[GetMeeting], summary="Получить список собраний."
)
async def get_meetings(uow: UoWDep):
    """Получение списка всех собраний."""
    return await MeetingServices().get_meetings(uow)


@router.post("/", response_model=GetMeeting, summary="Создание собрания.")
async def create_meeting(uow: UoWDep, meeting: MeetingCreate):
    """Создать собрание."""
    try:
        return await MeetingServices().create_meeting(uow, meeting)
    except InvalidDate:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Дата собрания не может быть меньше текущей.",
        )


@router.patch(
    "/{id}", response_model=GetMeeting, summary="Редактирование собрания."
)
async def update_meeting(uow: UoWDep, id: int, meeting: MeetingUpdate):
    try:
        return await MeetingServices().update_meeting(uow, id, meeting)
    except InvalidDate:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Дата собрания не может быть меньше текущей.",
        )
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытое собрание нельзя редактировать.",
        )


@router.delete("/{id}", response_model=GetMeeting, summary="Удалить собрание.")
async def delete_meeting(uow: UoWDep, id: int):
    """Удалить собрание с указанным id."""
    try:
        return await MeetingServices().delete_meeting(uow, id)
    except ObjectIsNoneException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Собрания с таким id не существует!",
        )
    except MeetingClosed:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытое собрание нельзя удалить.",
        )


@router.get(
    "/{id}/participants",
    response_model=MeetingParticipants,
    summary="Список записавшихся на собрание.",
)
async def get_participants_list(uow: UoWDep, id: int):
    try:
        return await MeetingServices().get_participants(uow, id)
    except ObjectIsNoneException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Собрания с таким id не существует!",
        )
