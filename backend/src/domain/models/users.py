from sqlalchemy import Column, String

from src.infrastructure.db import Base


class User(Base):
    """Модель пользователя."""

    name = Column(String(255), nullable=False)
    phone = Column(String(11), unique=True)
    email = Column(String(255), unique=True, nullable=False)
