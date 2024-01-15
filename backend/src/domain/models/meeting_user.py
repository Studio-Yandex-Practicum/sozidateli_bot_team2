from sqlalchemy import Column, ForeignKey, Integer

from src.infrastructure.db import Base


class MeetingUser(Base):
    """Модель для записи пользователей на собьрание."""

    meeting = Column(Integer, ForeignKey("meeting.id"))
    user = Column(Integer, ForeignKey("user.id"))
