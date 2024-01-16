from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db import Base


class User(Base):
    """Модель пользователя."""

    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
