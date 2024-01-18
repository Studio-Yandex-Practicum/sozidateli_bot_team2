from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.schemas import GetUser
from src.infrastructure.db import Base


class User(Base):
    """Модель пользователя."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"))
    meeting = relationship("Meeting", back_populates="users")

    def to_read_model(self) -> GetUser:
        attrs = self.__dict__.copy()
        attrs.pop("_sa_instance_state", None)
        return GetUser(**attrs)
