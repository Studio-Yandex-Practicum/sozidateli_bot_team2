from sqlalchemy import Boolean, Column, DateTime, Text

from src.infrastructure.db import Base


class Meeting(Base):
    """Модель собраний."""

    date = Column(DateTime, nullable=False)
    is_open = Column(Boolean, default=True)
    description = Column(Text)
