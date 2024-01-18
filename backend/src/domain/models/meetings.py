from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.schemas import GetMeeting
from src.infrastructure.db import Base


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
