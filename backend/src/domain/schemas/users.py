import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator


NUMBER_RE = r"^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$"


class UserCreate(BaseModel):
    """Pydantic-схема для создания пользователя."""

    name: str = Field(..., min_length=1, max_length=255)
    phone: str
    email: EmailStr

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match(NUMBER_RE, value):
            raise ValueError(
                "Номер телефона должен состоять только из 11 цифр."
            )
        return value


class UserDB(UserCreate):
    """Pydantic-схема для базы данных."""

    model_config = ConfigDict(from_attributes=True)

    id: int
