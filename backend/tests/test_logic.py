import pytest
from httpx import AsyncClient

from src.main import app
from src.application.services.users import UserService
#from src.infrastructure.db import testing_async_session_maker
#from src.domain.models import User


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url='http://test') as client:
        new_user_data: UserService = {
            'id': 1,
            'name': 'test',
            'phone': '12345678990',
            'email': 'a@a.ru',
            'meeting_id': 1,
            'assistance_segment': 'not_decide',
            'meeting': '2022-01-01',
        }
        response = await client.post('/users/', json=new_user_data)
        assert response.status_code == 201
        assert response.json() == new_user_data
