from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4
from app.schemas.notification import NotificationCreate

import pytest

from app.models.notification import Notification
from app.services.notification_services import NotificationService, NotificationFilter


@pytest.fixture
def notification_service(mock_db_session):
    return NotificationService(mock_db_session)


@pytest.mark.asyncio
async def test_create_notification(notification_service, mock_db_session):
    user_id = uuid4()
    data = NotificationCreate(
        user_id=user_id,
        title="Test Notification",
        text="This is a test"
    )

    db_notification = Notification(
        id=uuid4(),
        user_id=user_id,
        title=data.title,
        text=data.text,
        created_at=datetime.utcnow(),
        processing_status="pending"
    )

    mock_db_session.add = AsyncMock()
    mock_db_session.commit = AsyncMock()
    mock_db_session.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, "id", db_notification.id))

    result = await notification_service.create_notification(data)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

    assert result.title == "Test Notification"
    assert result.user_id == user_id


@pytest.mark.asyncio
async def test_get_notifications(mock_db_session, mock_execute_result_all):
    mock_notifications = [
        Notification(
            id=uuid4(),
            user_id=uuid4(),
            title="Test 1",
            text="This is a test 1",
            created_at=datetime.utcnow(),
            processing_status="completed",
        ),
        Notification(
            id=uuid4(),
            user_id=uuid4(),
            title="Test 2",
            text="This is a test 2",
            created_at=datetime.utcnow(),
            processing_status="pending",
        ),
    ]

    mock_db_session.execute = mock_execute_result_all(mock_notifications)
    service = NotificationService(mock_db_session)
    filters = NotificationFilter()

    result = await service.get_notifications(filters=filters)

    assert result[0].title == "Test 1"
    assert result[1].title == "Test 2"
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_notification_by_id(mock_db_session, mock_execute_result):
    mock_notification = Notification(
        id=uuid4(),
        user_id=uuid4(),
        title="Test Notification",
        text="This is a test",
        created_at=datetime.utcnow(),
        processing_status="completed",
    )

    mock_db_session.execute = mock_execute_result(mock_notification)
    service = NotificationService(mock_db_session)

    result = await service.get_notification_by_id(mock_notification.id)

    assert result.id == mock_notification.id