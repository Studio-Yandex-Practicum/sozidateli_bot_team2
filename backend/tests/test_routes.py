import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_users_root():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/users/')
        assert response.status_code == 200, 'Не доступен endpoint /users/'


@pytest.mark.asyncio
async def test_meetings_root():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/meetings/')
        assert response.status_code == 200, 'Не доступен endpoint /meetings/'
