from src.application.protocols.unit_of_work import UoW
from src.core.exceptions import (
    MeetingClosed,
    ObjectAlreadyExists,
    ObjectIsNoneException,
)
from src.domain.schemas import GetUser, UserCreate, UserUpdate


class UserService:
    async def _validate_user_exists(
        self, uow: UoW, search_params: dict
    ) -> None:
        """Проверка уникальности пользователя."""
        if not search_params:
            return
        async with uow:
            user = await uow.users.find_all_by_attrs(**search_params)
        if user:
            raise ObjectAlreadyExists

    async def _validate_meeting_exists(self, uow: UoW, id: int) -> None:
        """Проверка что собрание с таким id существует."""
        meeting = await uow.meetings.find_one(id=id)
        if not meeting:
            raise ObjectIsNoneException

    async def _validate_meeting_is_open(self, uow: UoW, id: int) -> None:
        """Проверка что запись на собрание открыта."""
        meeting = await uow.meetings.find_one(id=id)
        if not meeting.is_open:
            raise MeetingClosed

    async def get_users(self, uow: UoW) -> list[GetUser]:
        """Получить список пользователей."""
        async with uow:
            users = await uow.users.find_all()
            return [user.to_read_model() for user in users]

    async def get_user(self, uow: UoW, id: int) -> GetUser:
        """Получить пользователя по id."""
        async with uow:
            user = await uow.users.find_one(id=id)
            return user.to_read_model()

    async def create_user(self, uow: UoW, schema: UserCreate) -> GetUser:
        """Создать пользователя."""
        user_data = schema.model_dump(exclude_none=True)

        meeting_id = user_data.pop("meeting_id", None)
        async with uow:
            await self._validate_meeting_exists(uow, meeting_id)
            await self._validate_meeting_is_open(uow, meeting_id)

        assistance_segment = user_data.pop("assistance_segment", None)

        await self._validate_user_exists(uow, user_data)

        user_data["meeting_id"] = meeting_id
        user_data["assistance_segment"] = assistance_segment

        async with uow:
            user = await uow.users.add_one(**user_data)
            await uow.commit()
            return user.to_read_model()

    async def update_user(
        self, uow: UoW, id: int, schema: UserUpdate
    ) -> GetUser:
        """Обновить инфо о пользователе."""
        user_data = schema.model_dump(exclude_none=True)

        meeting_id = user_data.pop("meeting_id", None)
        assistance_segment = user_data.pop("assistance_segment", None)

        await self._validate_user_exists(uow, user_data)

        if assistance_segment:
            user_data["assistance_segment"] = assistance_segment

        if meeting_id:
            if meeting_id > 0:
                user_data["meeting_id"] = meeting_id
                async with uow:
                    await self._validate_meeting_exists(uow, meeting_id)
                    await self._validate_meeting_is_open(uow, meeting_id)
            else:
                raise ObjectIsNoneException

        async with uow:
            user = await uow.users.update_one(id=id, **user_data)
            await uow.commit()
            return user.to_read_model()

    async def delete_user(self, uow: UoW, id: int) -> GetUser:
        """Удалить пользователя."""
        async with uow:
            user = await uow.users.find_one(id=id)
            if not user:
                raise ObjectIsNoneException
            user = await uow.users.delete_one(id=id)
            await uow.commit()
            return user.to_read_model()
