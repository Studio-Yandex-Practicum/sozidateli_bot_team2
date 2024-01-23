import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


NUMBER_RE = r"^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$"


class GetUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: EmailStr
    meeting_id: int


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str
    email: EmailStr
    meeting_id: int

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.match(NUMBER_RE, value):
            raise ValueError(
                "Номер телефона должен состоять только из 11 цифр."
            )
        return value


class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    meeting_id: int | None = None
