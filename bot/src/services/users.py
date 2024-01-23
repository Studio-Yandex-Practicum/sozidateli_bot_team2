from collections import Generator
from http import HTTPStatus

import aiohttp
from aiohttp import ClientResponse

from src.core import settings
from src.schemas import users
from src.services.exceptions import HTTPRequestError


class UserService:
    def __init__(self):
        self._path = '/users'

    async def get_users(self) -> Generator[users.GetUser]:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.get(self._path) as response:
                return await self._get_users(response)

    async def create_user(self, user: users.UserCreate) -> users.GetUser:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.post(self._path,
                                    data=user.model_dump()) as response:
                return await self._get_user(response)

    async def update_user(self, id: int,
                          user: users.UserUpdate) -> users.GetUser:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.post(f'self._path/{id}',
                                    data=user.model_dump()) as response:
                return await self._get_user(response)

    async def delete_user(self, id: int):
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.delete(f'{self._path}/{id}') as response:
                if not (response.status == HTTPStatus.OK):
                    raise HTTPRequestError('Ошибка запроса! Повторите снова!')

    async def _get_user(self,
                        response: ClientResponse) -> users.GetUser:
        if response.status == HTTPStatus.OK:
            return users.GetUser(**(await response.json()))
        raise HTTPRequestError('Ошибка запроса! Повторите снова!')

    async def _get_users(
            self, response: ClientResponse
    ) -> Generator[users.GetUser]:
        if response.status == HTTPStatus.OK:
            return (users.GetUser(**json) for json in
                    await response.json())
        raise HTTPRequestError('Ошибка запроса! Повторите снова!')
