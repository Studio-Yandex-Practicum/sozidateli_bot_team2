from src.application.protocols.unit_of_work import UoW


class UserService:
    async def get_users(self, uow: UoW):
        async with uow:
            ...
