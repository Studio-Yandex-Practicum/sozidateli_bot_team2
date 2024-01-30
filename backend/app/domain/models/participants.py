from app.domain.schemas import GetParticipant
from app.infrastructure.db import Base
from fastapi import Request
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import AssistanceSegment


class Participant(Base):
    """Модель участника."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    assistance_segment: Mapped[AssistanceSegment] = mapped_column(
        Enum(AssistanceSegment), default=AssistanceSegment.not_decide
    )
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"))
    meeting = relationship("Meeting", back_populates="participants")

    async def __admin_repr__(self, _: Request):
        return f"{self.name}"

    def to_read_model(self) -> GetParticipant:
        attrs = self.__dict__.copy()
        attrs.pop("_sa_instance_state", None)
        return GetParticipant(**attrs)
