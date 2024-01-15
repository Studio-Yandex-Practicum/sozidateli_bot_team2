import re

from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    """Pydantic-схема для создания пользователя."""

    name: str = Field(..., min_length=1, max_length=255)
    phone: str
    email: EmailStr

    @validator("phone")
    def validate_phone(cls, value):
        if not re.match("^[0-9]{11}$", value):
            raise ValueError(
                "Номер телефона должен состоять только из 11 цифр."
            )
        return value


class UserDB(UserCreate):
    """Pydantic-схема для базы данных."""

    id: int

    class Config:
        from_attributes = True
