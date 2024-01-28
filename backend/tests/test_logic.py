import pytest
from httpx import AsyncClient

from src.main import app
from src.application.services.users import UserService
#from src.infrastructure.db import testing_async_session_maker
#from src.domain.models import User


@pytest.mark.parametrize('json', [
  {"date": "2024-01-30T15:15:45.848Z",
   "description": "Описание встречи"}
])
async def test_post_meeting(async_client: AsyncClient, json):
    response = await async_client.post('/meetings/')
    assert response.status_code == 200, 'Код запроса вернулся неверный!'
    data = response.json()
    keys = sorted(['id', 'date', 'is_open', 'description'])
    assert keys == sorted(data.keys()), 'Ключи в ответе не совпадают'


@pytest.mark.parametrize('json', [
    {'name': 'test', 'phone': '12345678990',
     'email': 'a@a.ru', 'meeting_id': 1,
     'assistance_segment': 'Детям в детских домах'}
])
async def test_create_user(async_client: AsyncClient, json):
    response = await async_client.post('/users/')
    assert response.status_code == 200, 'Не удалось создать пользователя'
