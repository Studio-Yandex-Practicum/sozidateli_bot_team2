import datetime as dt
from zoneinfo import ZoneInfo

from src.application.protocols.unit_of_work import UoW
from src.core.constants import DATE_FORMAT, ZONEINFO
from src.core.exceptions import (
    InvalidDate,
    ObjectIsNoneException,
)
from src.domain.schemas import (
    GetMeeting,
    MeetingCreate,
    MeetingParticipants,
    MeetingUpdate,
)
from .base import BaseService


class MeetingServices(BaseService):
    async def get_meetings(self, uow: UoW) -> list[GetMeeting]:
        """Получить список собраний."""
        async with uow:
            meetings = await uow.meetings.find_all()
            return [meeting.to_read_model() for meeting in meetings]

    async def get_meeting(self, uow: UoW, id: int) -> GetMeeting:
        """Получить собрание по id."""
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            return meeting.to_read_model()

    async def create_meeting(
            self, uow: UoW, schema: MeetingCreate
    ) -> GetMeeting:
        """Создать собрание."""
        self._validate_meeting_date(schema.date)
        async with uow:
            meeting = await uow.meetings.add_one(**schema.model_dump())
            await uow.commit()
            return meeting.to_read_model()

    async def update_meeting(
            self, uow: UoW, id: int, schema: MeetingUpdate
    ) -> GetMeeting:
        """Обновить информацию о собрании."""
        if schema.date:
            self._validate_meeting_date(schema.date)
        async with uow:
            await self._check_meeting(id, uow)
            meeting = await uow.meetings.update_one(
                id=id, **schema.model_dump(exclude_none=True)
            )
            await uow.commit()
            return meeting.to_read_model()

    async def delete_meeting(self, uow: UoW, id: int) -> GetMeeting:
        """Удалить собрание."""
        async with uow:
            await self._check_meeting(id, uow)
            meeting = await uow.meetings.delete_one(id=id)
            await uow.commit()
            return meeting.to_read_model()

    async def get_participants(self, uow: UoW, id: int) -> MeetingParticipants:
        """Получить список участников собрания."""
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            if not meeting:
                raise ObjectIsNoneException()
            participants = MeetingParticipants(
                id=meeting.id,
                date=meeting.date,
                is_open=meeting.is_open,
                description=meeting.description,
                users=[
                    user.to_read_model() for user in await uow.users.find_all(
                        meeting_id=id
                    )
                ],
            )
            return participants

    def _validate_meeting_date(self, date) -> None:
        if date.strftime(DATE_FORMAT) < dt.datetime.now(
                tz=ZoneInfo(ZONEINFO)
        ).strftime(DATE_FORMAT):
            raise InvalidDate()
