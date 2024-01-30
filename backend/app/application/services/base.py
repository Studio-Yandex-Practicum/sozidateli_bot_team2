from typing import Any, TypeVar

from app.application.protocols.unit_of_work import UoW
from app.core.exceptions import MeetingClosed, ObjectIsNoneException
from pydantic import BaseModel


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseService:
    async def _check_meeting(self, id: int, uow: UoW):
        meeting = await uow.meetings.find_one(id=id)
        if not meeting:
            raise ObjectIsNoneException()
        if not meeting.is_open:
            raise MeetingClosed()
