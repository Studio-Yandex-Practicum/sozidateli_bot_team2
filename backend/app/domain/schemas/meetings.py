import datetime as dt

from pydantic import BaseModel, ConfigDict

from .users import GetUser


class BaseMeeting(BaseModel):
    date: dt.datetime | None = None
    is_open: bool | None = None
    description: str | None = None


class MeetingCreate(BaseModel):
    date: dt.datetime
    description: str | None = None


class GetMeeting(BaseMeeting):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: dt.datetime
    is_open: bool


class MeetingUpdate(BaseMeeting):
    ...


class MeetingParticipants(BaseModel):
    id: int
    date: dt.datetime
    is_open: bool
    description: str
    users: list[GetUser]
