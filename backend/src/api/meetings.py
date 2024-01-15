from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.application.repositories import BaseRepository
from src.containers import Container
from src.domain.schemas import MeetingCreate, MeetingDB


router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get(
    "/", response_model=list[MeetingDB], summary="Получить список собраний."
)
@inject
async def get_meetings(
    meeting_repository: BaseRepository = Depends(
        Provide[Container.meeting_repository]
    ),
):
    """Получение списка всех собраний."""
    return await meeting_repository.get_list()


@router.post("/", response_model=MeetingDB, summary="Создание собрания.")
@inject
async def create_meeting(
    meeting: MeetingCreate,
    meeting_repository: BaseRepository = Depends(
        Provide[Container.meeting_repository]
    ),
):
    """Создать собрание."""
    new_meeting = await meeting_repository.create(meeting)
    return new_meeting


@router.delete(
    "/{meeting_id}", response_model=MeetingDB, summary="Удалить собрание."
)
@inject
async def delete_meeting(
    meeting_id: int,
    meeting_repository: BaseRepository = Depends(
        Provide[Container.meeting_repository]
    ),
):
    """Удалить собрание с указанным id."""
    meeting = await meeting_repository.get_by_attributes(id=meeting_id)
    return await meeting_repository.remove(meeting)
