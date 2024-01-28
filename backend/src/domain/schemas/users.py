import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from src.core.constants import NUMBER_PATTERN
from src.domain.models.enums import AssistanceSegment



class BaseUser(BaseModel):
    name: str
    phone: str
    email: EmailStr
    meeting_id: int


class GetUser(BaseUser):
    model_config = ConfigDict(from_attributes=True)

    id: int
    assistance_segment: AssistanceSegment


class UserCreate(BaseUser):
    name: str = Field(..., min_length=1, max_length=255)
    phone: str
    assistance_segment: AssistanceSegment

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.match(NUMBER_PATTERN, value):
            raise ValueError(
                "Номер телефона должен состоять только из 11 цифр."
            )
        return value


class UserUpdate(UserCreate):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    meeting_id: int | None = None
    assistance_segment: AssistanceSegment | None = None
