import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('meeting_data', [
  {"date": "2024-01-30T15:15:45.848Z",
   "description": "Meeting description"}
])
async def test_create_meeting(async_client: AsyncClient, meeting_data: dict):
    response = await async_client.post('/meetings/', json=meeting_data)
    assert response.status_code == 200, 'Некорректный код ответа!'
    data = response.json()
    keys = sorted(['id', 'date', 'is_open', 'description'])
    assert keys == sorted(data.keys()), 'Ключи в ответе не найдены!'


@pytest.mark.parametrize('user', [
    {"name": "Саша", "phone": "+79999999999",
     "email": "sasha@test.ru", "meeting_id": 1,
     "assistance_segment": "Детям в детских домах"}
])
async def test_create_user(async_client: AsyncClient, user: dict):
    response = await async_client.post('/users/', json=user)
    assert response.status_code == 200, 'Не удалось создать пользователя'


@pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient):
    response = await async_client.get('/users/')
    assert response.status_code == 200, 'Не доступен endpoint /users/'
    assert len(response.json()) > 0, 'Пользователи не найдены'


@pytest.mark.asyncio
async def test_get_meetings(async_client: AsyncClient):
    response = await async_client.get('/meetings/')
    assert response.status_code == 200, 'Не доступен endpoint /meetings/'
    assert len(response.json()) > 0, 'Собрания не найдены'


@pytest.mark.parametrize('meeting_id', [
    1,
])
@pytest.mark.parametrize('new_meetind_data', [
    {"description": "new description"}
])
async def test_patch_meeting(async_client: AsyncClient, meeting_id: int,
                             new_meetind_data: dict):
    response = await async_client.patch(f'/meetings/{meeting_id}',
                                        json=new_meetind_data)
    assert response.status_code == 200, 'Некорректный код ответа!'
    data = response.json()
    new_description = new_meetind_data['description']
    assert data['description'] == new_description, 'Некорректное описание!'


@pytest.mark.parametrize('user_id', [
    1,
])
@pytest.mark.parametrize('new_user_data', [
    {"phone": "+79999999990"}
])
async def test_patch_user(async_client: AsyncClient, user_id: int,
                          new_user_data: dict):
    response = await async_client.patch(f'/users/{user_id}',
                                        json=new_user_data)
    assert response.status_code == 200, 'Некорректный код ответа!'
    data = response.json()
    new_phone = new_user_data['phone']
    assert data['phone'] == new_phone, 'Некорректный телефон!'


@pytest.mark.parametrize('user_id', [
    1,
])
async def test_delete_user(async_client: AsyncClient, user_id: int):
    response = await async_client.delete(f'/users/{user_id}')
    assert response.status_code == 200, 'Некорректный код ответа!'
    data = response.json()
    assert data['id'] == user_id, 'Некорректный id пользователя!'


@pytest.mark.parametrize('meeting_id', [
    1,
])
async def test_delete_meeting(async_client: AsyncClient, meeting_id: int):
    response = await async_client.delete(f'/meetings/{meeting_id}')
    assert response.status_code == 200, 'Некорректный код ответа!'
    data = response.json()
    assert data['id'] == meeting_id, 'Некорректный id собрания!'
