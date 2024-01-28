import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('meeting_data_1', [
  {"date": "2026-01-30T15:15:45.848Z",
   "description": "Meeting description"}
])
@pytest.mark.parametrize('meeting_data_2', [
  {"date": "2027-01-30T15:15:45.848Z",
   "description": "Meeting description"}
])
async def test_create_meeting(async_client: AsyncClient,
                              meeting_data_1: dict, meeting_data_2: dict):
    response = await async_client.post('/meetings/', json=meeting_data_1)
    assert response.status_code == 200, 'Некорректный код ответа!'
    response = await async_client.post('/meetings/', json=meeting_data_2)
    assert response.status_code == 200, 'Некорректный код ответа!'
    response = await async_client.get('/meetings/')
    assert response.status_code == 200, 'Некорректный код ответа!'
    assert len(response.json()) == 2, 'Некорректное количество собраний!'


@pytest.mark.parametrize('user_1', [
    {"name": "Вася", "phone": "+79999999000",
     "email": "vasya@test.ru", "meeting_id": 1,
     "assistance_segment": "Детям в детских домах"}
])
@pytest.mark.parametrize('user_2', [
    {"name": "Петя", "phone": "+79999999001",
     "email": "petya@test.ru", "meeting_id": 1,
     "assistance_segment": "Детям в детских домах"}
])
async def test_users_content(async_client: AsyncClient,
                             user_1: dict, user_2: dict):
    response = await async_client.post('/users/', json=user_1)
    assert response.status_code == 200, 'Не удалось создать Васю!'
    response = await async_client.post('/users/', json=user_2)
    assert response.status_code == 200, 'Не удалось создать Петю!'
    response = await async_client.get('/users/')
    assert response.status_code == 200, 'Не удалось получить пользователей!'
    assert len(response.json()) == 2, 'Некорректное количество пользователей!'
