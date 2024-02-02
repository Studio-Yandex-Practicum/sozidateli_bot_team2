import pytest
from httpx import AsyncClient
from contextlib import nullcontext as does_not_raise


class TestMeetingApi:
    @pytest.fixture(scope="class")
    async def create_participants(self, async_client: AsyncClient):
        participant_1 = {
            "name": "Вася",
            "phone": "+79999999000",
            "email": "vasya@test.ru",
            "meeting_id": 1,
            "assistance_segment": "Детям в детских домах",
        }
        participant_2 = {
            "name": "Петя",
            "phone": "+79999999001",
            "email": "petya@test.ru",
            "meeting_id": 1,
            "assistance_segment": "Еще не определился",
        }
        await async_client.post("/users/", json=participant_1)
        await async_client.post("/users/", json=participant_2)
        response = await async_client.get("/users/")
        print(response.json())
        yield
        await async_client.delete("/users/1")
        await async_client.delete("/users/2")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "meetings",
        [
            {
                "date": "2034-02-02T15:25:04.424Z",
                "description": "Собрание модных обжэшников.",
            },
            {
                "date": "2034-02-03T15:25:04.424Z",
            },
        ],
    )
    async def test_create_correct_meetings(
        self, async_client: AsyncClient, meetings
    ):
        response = await async_client.post("/meetings/", json=meetings)
        assert (
            response.status_code == 200
        ), f'Не удалось создать собрание {meetings["date"]}!'

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_meetings, expectation",
        [
            ({"date": "2024-02-01T15:25:04.424Z"}, pytest.raises(TypeError)),
            ({}, does_not_raise()),
        ],
    )
    async def test_create_incorrect_meetings(
        self, async_client: AsyncClient, wrong_meetings, expectation
    ):
        with expectation:
            response = await async_client.post(
                "/meetings/", json=wrong_meetings
            )
            assert response.status_code in (
                400,
                422,
                500,
            ), "Неожиданное поведение."

    @pytest.mark.asyncio
    async def test_get_meetings(self, async_client: AsyncClient):
        response = await async_client.get("/meetings/")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_meeting_by_id(self, async_client: AsyncClient):
        response = await async_client.get("/meetings/1")
        assert response.json().get("date") == "2034-02-02T15:25:04.424000"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "meetings",
        [
            {"date": "2032-02-02T15:25:04.424Z"},
            {"description": "Это какое-то ново описание."},
        ],
    )
    async def test_patch_meeting_with_valid_data(
        self, async_client: AsyncClient, meetings
    ):
        response = await async_client.patch("/meetings/1", json=meetings)
        assert response.status_code == 200

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "wrong_meetings", [{"date": "2012-02-02T15:25:04.424Z"}]
    )
    async def test_patch_meeting_with_invalid_data(
        self, async_client: AsyncClient, wrong_meetings
    ):
        response = await async_client.patch("/meetings/1", json=wrong_meetings)
        assert response.status_code in (
            400,
            422,
        ), "Неожиданное поведение при неправильных данных."

    @pytest.mark.asyncio
    async def test_delete_meeting(self, async_client: AsyncClient):
        response = await async_client.delete("/meetings/2")
        assert response.status_code == 200, "Ошибка при удалении собрания."

    @pytest.mark.asyncio
    async def test_get_participants_of_meeting(
        self, async_client: AsyncClient, create_participants
    ):
        response = await async_client.get("/meetings/1/participants")
        assert len(response.json().get("users")) == 2
