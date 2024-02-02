import pytest
from httpx import AsyncClient


class TestUserApi:
    @pytest.fixture(scope="class")
    async def create_meetings(self, async_client: AsyncClient):
        meeting1 = {
            "date": "2070-02-02T12:55:36.672Z",
            "description": "Hello from future",
        }
        meeting2 = {
            "date": "2070-02-03T12:55:36.672Z",
            "description": "Hello from future 2",
        }
        await async_client.post("/meetings/", json=meeting1)
        await async_client.post("/meetings/", json=meeting2)
        yield

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user_data",
        [
            {
                "name": "Вася",
                "phone": "+79999999000",
                "email": "vasya@test.ru",
                "meeting_id": 1,
                "assistance_segment": "Детям в детских домах",
            },
            {
                "name": "Петя",
                "phone": "+79999999001",
                "email": "petya@test.ru",
                "meeting_id": 2,
                "assistance_segment": "Еще не определился",
            },
        ],
    )
    async def test_create_correct_users(
        self, async_client: AsyncClient, user_data, create_meetings
    ):
        response = await async_client.post("/users/", json=user_data)
        assert (
            response.status_code == 200
        ), f'Не удалось создать пользователя {user_data["name"]}!'

    @pytest.mark.parametrize(
        "wrong_users",
        [
            {
                "name": "Black Vlastelin",
                "phone": "phone",
                "email": "black@test.ru",
                "meeting_id": 1,
                "assistance_segment": "Могу автоволонтерить",
            },
            {
                "name": "Black Vlastelin",
                "phone": "+79999999002",
                "email": "black@test",
                "meeting_id": 1,
                "assistance_segment": "Могу автоволонтерить",
            },
            {
                "name": "Black Vlastelin",
                "phone": "+79999999002",
                "email": "black@test.ru",
                "meeting_id": 100,
                "assistance_segment": "Могу автоволонтерить",
            },
            {
                "name": "Black Vlastelin",
                "phone": "+79999999002",
                "email": "black@test.ru",
                "meeting_id": 1,
                "assistance_segment": "Могу пить чай",
            },
            {
                "name": "Black Vlastelin",
                "phone": "+79999999002",
                "email": "black@test.ru",
                "meeting_id": 1,
            },
            {},
        ],
    )
    @pytest.mark.asyncio
    async def test_create_incorrect_user(
        self, async_client: AsyncClient, wrong_users
    ):
        response = await async_client.post("/users/", json=wrong_users)
        assert response.status_code in (
            400,
            422,
        ), "Неожиданный результат при создании участника с wrong данными."

    @pytest.mark.asyncio
    async def test_get_users(self, async_client: AsyncClient):
        response = await async_client.get("/users/")
        assert len(response.json()) == 2, "Неправильно работает метод GET."

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, async_client: AsyncClient):
        response = await async_client.get("/users/1")
        assert (
            response.json().get("name") == "Вася"
        ), "Неправильно работает получение данных пользователя по id."

    @pytest.mark.parametrize(
        "update_data",
        [
            {"name": "Ирина Вачовски"},
            {"phone": "+79999999003"},
            {"email": "vasya_is_irina_now@test.ru"},
            {"meeting_id": 2},
            {"assistance_segment": "Еще не определился"},
        ],
    )
    @pytest.mark.asyncio
    async def test_patch_user_with_valid_data(
        self, async_client: AsyncClient, update_data
    ):
        key, value = list(update_data.items())[0]
        response = await async_client.patch("/users/1", json=update_data)
        params = response.json()
        assert (
            params.get(key) == value
        ), "Неправильно работает изменение данных участника."

    @pytest.mark.parametrize(
        "update_data",
        [
            {"phone": "666"},
            {"email": "vasya_was_here"},
            {"meeting_id": 2000},
            {"assistance_segment": "Гладить котиков"},
        ],
    )
    @pytest.mark.asyncio
    async def test_patch_user_with_invalid_data(
        self, async_client: AsyncClient, update_data
    ):
        response = await async_client.patch("/users/1", json=update_data)
        assert response.status_code in (
            400,
            422,
        ), "Неправильное поведение при обновлении некорректными данными"
