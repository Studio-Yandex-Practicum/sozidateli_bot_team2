from datetime import datetime

from src.application.protocols.unit_of_work import UoW
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


DATE_FORMAT = "%d %m %Y %H:%M:%S"


class MeetingServices:
    async def validate_meeting_date(self, date) -> None:
        """Валидация даты. Должна быть в будущем."""
        if date.strftime(DATE_FORMAT) < datetime.now().strftime(DATE_FORMAT):
            raise InvalidDate

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
        await self.validate_meeting_date(schema.date)
        async with uow:
            meeting = await uow.meetings.add_one(**schema.model_dump())
            await uow.commit()
            return meeting.to_read_model()

    async def update_meeting(
        self, uow: UoW, id: int, schema: MeetingUpdate
    ) -> GetMeeting:
        """Обновить инфо о собрании."""
        if schema.date:
            await self.validate_meeting_date(schema.date)
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            if not meeting:
                raise ObjectIsNoneException
            if not meeting.is_open:
                raise MeetingClosed
            meeting = await uow.meetings.update_one(
                id=id, **schema.model_dump()
            )
            await uow.commit()
            return meeting.to_read_model()

    async def delete_meeting(self, uow: UoW, id: int) -> GetMeeting:
        """Удалить собрание."""
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            if not meeting:
                raise ObjectIsNoneException
            if not meeting.is_open:
                raise MeetingClosed
            meeting = await uow.meetings.delete_one(id=id)
            await uow.commit()
            return meeting.to_read_model()

    async def get_participants(self, uow: UoW, id: int) -> MeetingParticipants:
        """Получить список участников собрания."""
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            if not meeting:
                raise ObjectIsNoneException
            users = await uow.users.find_all_by_attrs(meeting_id=id)
            participants = MeetingParticipants(
                id=meeting.id,
                date=meeting.date,
                is_open=meeting.is_open,
                description=meeting.description,
                users=[user.to_read_model() for user in users],
            )
            return participants
