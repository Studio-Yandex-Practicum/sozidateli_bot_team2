from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeetingCreate(BaseModel):
    date: datetime
    description: str


class MeetingDB(BaseModel):
    """Pydantic-схема для базы данных."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
    description: str
