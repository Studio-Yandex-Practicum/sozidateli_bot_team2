from src.application.protocols.unit_of_work import UoW
from src.core.exceptions import (
    MeetingClosed,
    ObjectAlreadyExists,
    ObjectIsNoneException,
)
from src.domain.schemas import GetUser, UserCreate, UserUpdate


class UserService:
    async def validate_user_exists(self, uow: UoW, search_params):
        """Проверка уникальности пользователя."""
        search_params = {
            key: value for key, value in search_params if value is not None
        }
        if not search_params:
            return
        async with uow:
            user = await uow.users.find_all_by_attrs(**search_params)
        if user:
            raise ObjectAlreadyExists

    async def validate_meeting_exists(self, uow: UoW, id: int):
        """Проверка что собрание с таким id существует."""
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            if not meeting:
                raise ObjectIsNoneException

    async def validate_meeting_is_open(self, uow: UoW, id: int):
        """Проверка что запись на собрание открыта."""
        async with uow:
            meeting = await uow.meetings.find_one(id=id)
            if not meeting.is_open:
                raise MeetingClosed

    async def get_users(self, uow: UoW):
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
        meeting_id = schema.meeting_id
        await self.validate_meeting_exists(uow, meeting_id)
        del schema.meeting_id
        assistance_segment = schema.assistance_segment
        del schema.assistance_segment
        await self.validate_user_exists(uow, schema)
        schema.meeting_id = meeting_id
        schema.assistance_segment = assistance_segment
        await self.validate_meeting_is_open(uow, meeting_id)
        async with uow:
            user = await uow.users.add_one(**schema.model_dump())
            await uow.commit()
            return user.to_read_model()

    async def update_user(
        self, uow: UoW, id: int, schema: UserUpdate
    ) -> GetUser:
        """Обновить инфо о пользователе."""
        meeting_id = schema.meeting_id
        del schema.meeting_id
        if assistance_segment := schema.assistance_segment:
            del schema.assistance_segment
            await self.validate_user_exists(uow, schema)
            schema.assistance_segment = assistance_segment
        schema.meeting_id = meeting_id
        if meeting_id:
            if meeting_id > 0:
                await self.validate_meeting_exists(uow, meeting_id)
                await self.validate_meeting_is_open(uow, meeting_id)
            else:
                raise ObjectIsNoneException
        async with uow:
            user = await uow.users.update_one(id=id, **schema.model_dump())
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
