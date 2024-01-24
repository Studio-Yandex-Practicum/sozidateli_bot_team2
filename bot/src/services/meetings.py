from collections import Generator
from http import HTTPStatus

import aiohttp
from aiohttp import ClientResponse

from src.core import settings
from src.schemas import meetings
from src.services.exceptions import HTTPRequestError


class MeetingService:
    def __init__(self):
        self._path = '/meetings'

    async def get_meetings(self) -> Generator[meetings.GetMeeting]:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.get(self._path) as response:
                return await self._get_meetings(response)

    async def create_meeting(self,
                             meeting: meetings.MeetingCreate) -> meetings.GetMeeting:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.post(
                    self._path, data=meeting.model_dump()
            ) as response:
                if response.status == HTTPStatus.OK:
                    return meetings.GetMeeting(**(await response.json()))
                raise HTTPRequestError('Ошибка запроса! Повторите снова!')

    async def update_meeting(
            self,
            id: int,
            meeting: meetings.MeetingUpdate
    ) -> meetings.GetMeeting:
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.patch(
                    f'{self._path}/{id}', data=meeting.model_dump()
            ) as response:
                return await self._get_meeting(response)

    async def delete_meeting(self, id: int):
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.delete(f'{self._path}/{id}') as response:
                if not (response.status == HTTPStatus.OK):
                    raise HTTPRequestError('Ошибка запроса! Повторите снова!')

    async def get_participants_list(self, id: int):
        async with aiohttp.ClientSession(settings.url) as session:
            async with session.get(
                    f'{self._path}/{id}/participants') as response:
                if response.status == HTTPStatus.OK:
                    return meetings.MeetingParticipants(
                        **(await response.json()))
                raise HTTPRequestError('Ошибка запроса! Повторите снова!')

    async def _get_meeting(self,
                           response: ClientResponse) -> meetings.GetMeeting:
        if response.status == HTTPStatus.OK:
            return meetings.GetMeeting(**(await response.json()))
        raise HTTPRequestError('Ошибка запроса! Повторите снова!')

    async def _get_meetings(
            self, response: ClientResponse
    ) -> Generator[meetings.GetMeeting]:
        if response.status == HTTPStatus.OK:
            return (meetings.GetMeeting(**json) for json in
                    await response.json())
        raise HTTPRequestError('Ошибка запроса! Повторите снова!')
