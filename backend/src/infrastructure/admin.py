from typing import Any, Dict

from sqlalchemy import select
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette_admin import (
    BooleanField,
    DateTimeField,
    EmailField,
    EnumField,
    HasMany,
    HasOne,
    PhoneField,
    StringField,
    TextAreaField,
)
from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.i18n import I18nConfig

from src.core import Settings as settings
from src.domain.models import Meeting, User
from src.domain.models.assistance import AssistanceSegment
from src.domain.schemas import MeetingCreate, UserCreate
from src.infrastructure.db import async_session_maker

from .db import engine
from .provider import UsernameAndPasswordProvider


class UserView(ModelView):
    """Модель отображения пользователя в админке."""

    identity = "user"

    fields = [
        StringField("name", label="Имя", required=True),
        PhoneField("phone", label="Номер телефона", required=True),
        EmailField("email", required=True),
        EnumField(
            "assistance_segment",
            label="Направление помощи",
            enum=AssistanceSegment,
        ),
        HasOne("meeting", label="Собрание", identity="meeting", required=True),
    ]
    label = "Участники"
    sortable_fields = [User.meeting]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        if data["meeting"] is None:
            raise FormValidationError(
                {"meeting": "Надо выбрать дату собрания."}
            )
        meeting = data.pop("meeting")
        user_attrs = {
            User.name: "name",
            User.phone: "phone",
            User.email: "email",
        }
        for attr, attr_name in user_attrs.items():
            async with async_session_maker() as session:
                users = await session.execute(
                    select(User).where(attr == data[attr_name])
                )
            if users.scalars().all():
                raise FormValidationError(
                    {attr_name: "Уже есть участник с такими данными."}
                )
        data["meeting_id"] = meeting.id
        await super().validate(request, data)
        if assistance_segment_value := data.get("assistance_segment"):
            assistance_segment_key = AssistanceSegment(
                assistance_segment_value
            ).name
            data["assistance_segment"] = assistance_segment_key
        data.pop("meeting_id")
        data["meeting"] = meeting


class MeetingView(ModelView):
    """Модель для отображения собраний в админке."""

    identity = "meeting"

    fields = [
        DateTimeField("date", label="Дата и время"),
        BooleanField("is_open", label="Закрыто/Открыто"),
        TextAreaField("description", label="Описание собрания"),
        HasMany("users", label="Участники собрания", identity="user"),
    ]
    label = "Собрания"
    sortable_fields = ["date", "is_open"]
    fields_default_sort = ["date", ("is_open", True)]


admin = Admin(
    engine,
    title="Проект 'Созидатели'",
    i18n_config=I18nConfig(default_locale="ru"),
    middlewares=[
        Middleware(
            SessionMiddleware, secret_key=settings.admin_middleware_secret
        )
    ],
    auth_provider=UsernameAndPasswordProvider(),
)

admin.add_view(UserView(User, pydantic_model=UserCreate, icon="fa fa-user"))

admin.add_view(
    MeetingView(Meeting, pydantic_model=MeetingCreate, icon="fa fa-calendar")
)
