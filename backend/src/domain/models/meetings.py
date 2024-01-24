from datetime import datetime

from fastapi import Request
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.schemas import GetMeeting
from src.infrastructure.db import Base


DATE_FORMAT = "%d.%m.%Y %H:%M"


class Meeting(Base):
    """Модель собраний."""

    date: Mapped[datetime] = mapped_column(nullable=False)
    is_open: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str] = mapped_column()
    users = relationship("User", back_populates="meeting")

    def to_read_model(self) -> GetMeeting:
        attrs = self.__dict__.copy()
        attrs.pop("_sa_instance_state", None)
        return GetMeeting(**attrs)

    async def __admin_repr__(self, request: Request):
        return f"{self.date.strftime(DATE_FORMAT)}"
