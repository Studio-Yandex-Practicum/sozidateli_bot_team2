import datetime as dt
from dataclasses import dataclass
from typing import Any
from zoneinfo import ZoneInfo

from app.application.repositories.participants import ParticipantRepository
from app.core import Settings as settings
from app.core.constants import DATE_FORMAT, ZONEINFO
from app.domain.models import Meeting, Participant
from app.domain.models.enums import AssistanceSegment
from app.domain.schemas import MeetingCreate, ParticipantCreate
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

from .db import engine
from .provider import UsernameAndPasswordProvider


@dataclass
class EnumCustomField(EnumField):
    def _get_label(self, value: Any, request: Request) -> Any:
        for v, label in self._get_choices(request):
            if value == getattr(AssistanceSegment, v):
                return label
        raise ValueError(f"Invalid choice value: {value}")


class ParicipantView(ModelView):
    """Модель отображения пользователя в админке."""

    identity = "participant"

    fields = [
        StringField("name", label="Имя", required=True),
        PhoneField("phone", label="Номер телефона", required=True),
        EmailField("email", required=True),
        EnumCustomField(
            "assistance_segment",
            label="Направление помощи",
            choices=[
                ("children_in_hospital", "Детям в больницах"),
                ("children_in_orphanages", "Детям в детских домах"),
                ("disabled_children", "Семьям с детьми-инвалидами"),
                ("auto_volunteer", "Могу автоволонтерить"),
                ("not_decide", "Еще не определился"),
            ],
            required=True,
        ),
        HasOne("meeting", label="Собрание", identity="meeting", required=True),
    ]
    label = "Участники"
    sortable_fields = [Participant.meeting]

    async def validate(self, request: Request, data: dict[str, Any]) -> None:
        errors: dict[str, str] = dict()
        if data["assistance_segment"] is None:
            errors["assistance_segment"] = "Нужно выбрать направление помощи."
        if data["meeting"] is None:
            errors["meeting"] = "Нужно выбрать собрание."
        if data["phone"] is None:
            errors["phone"] = "Нужно указать номер телефона."
        if data["name"] is None:
            errors["name"] = "Нужно указать имя участника."
        if data["email"] is None:
            errors["email"] = "Нужно укзать почту."

        self._change_assistance_segment(data)
        data["meeting_id"] = data["meeting"].id

        if request.state.action == "CREATE":
            await self._validate_create(request, data, errors)

        if len(errors) > 0:
            raise FormValidationError(errors)

        await super().validate(request, data)

    def _change_assistance_segment(self, data: dict[str, Any]):
        data["assistance_segment"] = getattr(
            AssistanceSegment, data["assistance_segment"]
        )

    async def _validate_create(
        self, request: Request, data: dict[str, Any], errors: dict[str, str]
    ):
        user_attrs = {
            "email": "Пользователя с данной почтой уже существует.",
            "phone": "Пользователь с данным телефоном уже существует.",
        }
        for key, value in user_attrs.items():
            if await ParticipantRepository(
                request.state.session
            ).check_user_exists(**{key: data[key]}):
                errors[key] = value


class MeetingView(ModelView):
    """Модель для отображения собраний в админке."""

    identity = "meeting"

    fields = [
        DateTimeField("date", label="Дата и время"),
        BooleanField("is_open", label="Закрыто/Открыто"),
        TextAreaField("description", label="Описание собрания"),
        HasMany(
            "participants", label="Участники собрания", identity="participant"
        ),
    ]
    label = "Собрания"
    sortable_fields = ["date", "is_open"]
    fields_default_sort = ["date", ("is_open", True)]

    async def validate(self, request: Request, data: dict[str, Any]) -> None:
        errors: dict[str, str] = dict()

        if data["date"] is None:
            errors["date"] = "Нужно указать дату собрания."
        if data["date"] and data["date"].strftime(
            DATE_FORMAT
        ) < dt.datetime.now(tz=ZoneInfo(ZONEINFO)).strftime(DATE_FORMAT):
            errors["date"] = "Дата собрания не может быть меньше текущей."
        if len(errors) > 0:
            raise FormValidationError(errors)

        await super().validate(request, data)


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

admin.add_view(
    ParicipantView(
        Participant, pydantic_model=ParticipantCreate, icon="fa fa-user"
    )
)

admin.add_view(
    MeetingView(Meeting, pydantic_model=MeetingCreate, icon="fa fa-calendar")
)
