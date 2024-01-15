from datetime import datetime

from pydantic import BaseModel


class MeetingCreate(BaseModel):
    date: datetime
    description: str


class MeetingDB(BaseModel):
    """Pydantic-схема для базы данных."""

    id: int
    date: datetime
    description: str

    class Config:
        from_attributes = True
