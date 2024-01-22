from typing import Any, Dict

from starlette.requests import Request
from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError

from src.domain.models import User, Meeting
from src.domain.schemas import UserCreate, MeetingCreate
from .db import engine


class UserView(ModelView):
    """Модель отображения пользователя в админке."""

    fields = ["name", "phone", "email", User.meeting]
    label = "Участники"
    sortable_fields = [User.meeting]
    searchable_fields = ["name", "phone", "email", User.meeting]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        if data["meeting"] is None:
            raise FormValidationError(
                {"meeting": "Надо выбрать дату собрания."}
            )
        meeting = data.pop("meeting")
        data["meeting_id"] = meeting.id
        await super().validate(request, data)
        data.pop("meeting_id")
        data["meeting"] = meeting


class MeetingView(ModelView):
    """Модель для отображения собраний в админке."""
    fields = ["date", "is_open", "description", Meeting.users]
    label = "Собрания"
    sortable_fields = ["date", "is_open"]
    searchable_fields = ["date"]
    fields_default_sort = ["date", ("is_open", True)]


admin = Admin(engine, title="Проект 'Созидатели'")

admin.add_view(UserView(User, icon="fa fa-user", pydantic_model=UserCreate))

admin.add_view(
    MeetingView(Meeting, icon="fa fa-calendar", pydantic_model=MeetingCreate)
)
