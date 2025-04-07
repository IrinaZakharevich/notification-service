import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationStatus, NotificationFilter
from app.tasks.tasks import analyze

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Сервис для работы с уведомлениями.

    Предоставляет бизнес-логику для создания, получения и обновления уведомлений.
    Взаимодействует с репозиторием уведомлений для работы с базой данных.
    """

    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса уведомлений.

        :param db: Асинхронная сессия базы данных.
        """
        self.repository = NotificationRepository(db)

    async def create_notification(
            self, notification: NotificationCreate
    ) -> NotificationRead:
        """
        Создает новое уведомление и запускает его асинхронную обработку.

        :param notification: Данные для создания уведомления
        :return: Сериализованное уведомление
        """
        try:
            db_notification = await self.repository.create(notification)
            analyze.delay(str(db_notification.id))
            return NotificationRead.model_validate(db_notification)
        except Exception as e:
            logger.exception(f"Error while creating notification: {e}")
            raise HTTPException(status_code=500, detail="Error creating notification")

    async def get_notifications(self, filters: NotificationFilter) -> list[NotificationRead]:
        """
        Возвращает список уведомлений с учетом фильтров и пагинации.

        :param skip: Количество уведомлений для пропуска (пагинация)
        :param limit: Максимальное количество уведомлений в ответе
        :param user_id: Фильтр по ID пользователя
        :param processing_status: Фильтр по статусу обработки
        :param category: Фильтр по категории
        :param start_date: Начальная дата создания уведомлений
        :param end_date: Конечная дата создания уведомлений
        :param read: Флаг прочитанности (True/False)
        :param confidence: Минимальный уровень уверенности
        :return: Список уведомлений, удовлетворяющих фильтрам
        """
        try:
            notifications = await self.repository.get_all(filters)
            return [NotificationRead.model_validate(notification) for notification in notifications]
        except Exception:
            logger.exception("Error while getting notifications")
            raise HTTPException(status_code=500, detail="Error retrieving notifications")

    async def get_notification_by_id(
            self, notification_id: UUID
    ) -> Optional[NotificationRead]:
        """
        Получает уведомление по его уникальному идентификатору.

        :param notification_id: UUID уведомления
        :return: Сериализованное уведомление или None, если не найдено
        """
        try:
            notification = await self.repository.get_by_id(notification_id)
            if notification:
                return NotificationRead.model_validate(notification)
            return None
        except Exception as e:
            logger.error(f"Error while getting notification: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving notification")

    async def update_read_status(
            self, notification_id: UUID
    ) -> NotificationRead:
        """
        Помечает уведомление как прочитанное.

        :param notification_id: UUID уведомления
        :return: Обновленное уведомление
        """
        try:
            db_notification = await self.repository.update_read_status(notification_id)
            if db_notification:
                return NotificationRead.model_validate(db_notification)
            raise HTTPException(status_code=404, detail="Notification not found")
        except Exception as e:
            logger.error(f"Error while updating read status: {e}")
            raise HTTPException(status_code=500, detail="Error updating notification status")

    async def get_notification_status(
            self, notification_id: UUID
    ) -> Optional[NotificationStatus]:
        """
        Получает текущий статус обработки уведомления.

        :param notification_id: UUID уведомления
        :return: Статус уведомления или None, если не найдено
        """
        try:
            status = await self.repository.get_status(notification_id)
            if status:
                return NotificationStatus(processing_status=status)
            return None
        except Exception as e:
            logger.error(f"Error while getting notification status: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving notification status")
