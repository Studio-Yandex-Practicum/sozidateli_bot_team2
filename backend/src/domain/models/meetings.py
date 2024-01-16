from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db import Base


class Meeting(Base):
    """Модель собраний."""

    date: Mapped[datetime] = mapped_column(nullable=False)
    is_open: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str] = mapped_column()
