import datetime as dt
from typing import Any
from zoneinfo import ZoneInfo

from starlette.requests import Request
from starlette_admin import (
    BooleanField,
    DateTimeField,
    HasMany,
    TextAreaField,
)
from starlette_admin import row_action
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError

from app.application.repositories.meetings import MeetingRepository
from app.core.constants import ZONEINFO
from app.core.parser import parser_date


class MeetingView(ModelView):
    """Модель для отображения собраний в админке."""

    identity = "meeting"

    row_actions = ['view', 'make_published', 'edit', 'delete']
    fields = [
        DateTimeField("date", label="Дата и время"),
        BooleanField("is_open", label="Закрыто/Открыто"),
        TextAreaField("description", label="Описание собрания"),
        HasMany("users", label="Участники собрания", identity="user"),
    ]
    label = "Собрания"
    sortable_fields = ["date", "is_open"]
    fields_default_sort = ["date", ("is_open", True)]

    @row_action(
        name="make_published",
        text="Получить дату с сайта",
        icon_class="fas fa-check-circle",
        submit_btn_text="Yes, proceed",
        submit_btn_class="btn-success",
        action_btn_class="btn-info",
        form="""
            <form>
                <div class="mt-3">
                    <input type="text" 
                           class="form-control" 
                           name="example-text-input" 
                           placeholder="Enter value">
                </div>
            </form>
            """,
    )
    async def make_published_row_action(self, request: Request, pk: Any) -> str:
        date = await parser_date()
        if date:
            session = request.state.session
            await MeetingRepository(session).add_one(date=date)
            await session.commit()
            return "Дата успешно получена с сайта!"
        return "Дату не удалось получить с сайта, добавьте вручную!"

    async def validate(self, request: Request, data: dict[str, Any]) -> None:
        """Валидация полей."""
        errors: dict[str, str] = dict()

        if data["date"] is None:
            errors["date"] = "Нужно указать дату собрания."

        if data["date"] and data["date"].replace(
                tzinfo=ZoneInfo(ZONEINFO)
        ).timestamp() < dt.datetime.now(
            tz=ZoneInfo(ZONEINFO)
        ).timestamp():
            errors["date"] = "Дата собрания не может быть меньше текущей."

        if len(errors) > 0:
            raise FormValidationError(errors)

        await super().validate(request, data)
