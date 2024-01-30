from app.application.protocols.unit_of_work import UoW
from app.core.exceptions import ObjectIsNoneException, UserAlreadyExists
from app.domain.schemas import (
    GetParticipant,
    ParticipantCreate,
    ParticipantUpdate,
)

from .base import BaseService


class ParticipantService(BaseService):
    async def get_users(self, uow: UoW) -> list[GetParticipant]:
        """Получить список пользователей."""
        async with uow:
            users = await uow.users.find_all()
            return [user.to_read_model() for user in users]

    async def get_user(self, uow: UoW, id: int) -> GetParticipant:
        """Получить пользователя по id."""
        async with uow:
            user = await uow.users.find_one(id=id)
            return user.to_read_model()

    async def create_user(
        self, uow: UoW, schema: ParticipantCreate
    ) -> GetParticipant:
        """Создать пользователя."""
        async with uow:
            await self._validate_user_exists(uow, schema.phone)
            await self._check_meeting(schema.meeting_id, uow)
            user = await uow.users.add_one(**schema.model_dump())
            await uow.commit()
            return user.to_read_model()

    async def update_user(
        self, uow: UoW, id: int, schema: ParticipantUpdate
    ) -> GetParticipant:
        """Обновить информацию о пользователе."""
        async with uow:
            await self._validate_user_exists(uow, schema.phone)
            if schema.meeting_id:
                await self._check_meeting(schema.meeting_id, uow)
            user = await uow.users.update_one(
                id=id, **schema.model_dump(exclude_none=True)
            )
            await uow.commit()
            return user.to_read_model()

    async def delete_user(self, uow: UoW, id: int) -> GetParticipant:
        """Удалить пользователя."""
        async with uow:
            await self._check_user(uow, id)
            user = await uow.users.delete_one(id=id)
            await uow.commit()
            return user.to_read_model()

    async def _validate_user_exists(
        self, uow: UoW, phone: str | None = None
    ) -> None:
        """Проверка уникальности пользователя."""
        if phone and await uow.users.find_one(phone=phone):
            raise UserAlreadyExists()

    async def _check_user(self, uow: UoW, id: int) -> None:
        if not await uow.users.find_one(id=id):
            raise ObjectIsNoneException()
