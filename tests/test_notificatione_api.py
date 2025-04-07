import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_create_notification(client: AsyncClient):
    response = await client.post(
        "/v1/notifications/",
        json={
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Test",
            "text": "Test message"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["processing_status"] == "pending"


@pytest.mark.asyncio
async def test_mark_notification_as_read(client: AsyncClient):
    notification_data = {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "Test",
        "text": "Test message"
    }

    create_response = await client.post("/v1/notifications/", json=notification_data)
    assert create_response.status_code == 200
    created_data = create_response.json()
    notification_id = created_data["id"]

    patch_response = await client.patch(f"/v1/notifications/{notification_id}/read")
    assert patch_response.status_code == 200
    updated_notification = patch_response.json()
    assert updated_notification["read_at"] is not None


@pytest.mark.asyncio
async def test_get_notifications(client: AsyncClient):
    # Создаем несколько уведомлений для тестирования
    user_id = str(uuid.uuid4())
    notification_data_1 = {
        "user_id": user_id,
        "title": "Test 1 warning",
        "text": "Test message 1",
    }
    notification_data_2 = {
        "user_id": str(uuid.uuid4()),
        "title": "Test 2",
        "text": "Test message 2",
    }

    # Отправляем POST-запросы для создания уведомлений
    await client.post("/v1/notifications/", json=notification_data_1)
    await client.post("/v1/notifications/", json=notification_data_2)

    # Запрашиваем все уведомления без фильтрации
    response = await client.get("/v1/notifications/")
    assert response.status_code == 200
    data = response.json()
    assert all("title" in item for item in data)

    # Запрашиваем уведомления с фильтрацией по user_id
    response = await client.get("/v1/notifications/", params={"user_id": user_id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_id

    # Проверка на отсутствие уведомлений по несуществующему user_id
    response = await client.get("/v1/notifications/", params={"user_id": str(uuid.uuid4())})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
