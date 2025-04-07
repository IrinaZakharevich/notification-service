from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationFilter


class NotificationRepository:
    """
    Репозиторий для работы с уведомлениями в базе данных.

    Предоставляет методы для создания, получения и обновления уведомлений.
    """

    def __init__(self, db: AsyncSession):
        """
        Инициализация репозитория.

        :param db: Асинхронная сессия базы данных.
        """
        self.db = db

    async def create(self, notification: NotificationCreate) -> Notification:
        """
        Создание нового уведомления.

        :param notification: Схема уведомления для создания.
        :return: Созданное уведомление.
        """
        db_notification = Notification(
            user_id=str(notification.user_id),
            title=notification.title,
            text=notification.text,
            created_at=datetime.utcnow(),
            processing_status="pending"
        )
        self.db.add(db_notification)
        await self.db.commit()
        await self.db.refresh(db_notification)
        return db_notification

    async def get_all(self, filters: NotificationFilter) -> List[Notification]:
        """
        Получение списка уведомлений с применением фильтров.

        :param filters: Фильтры для получения уведомлений.
        :return: Список уведомлений, соответствующих фильтрам.
        """
        stmt = select(Notification).options(selectinload("*"))

        conditions = []
        if filters.user_id:
            conditions.append(Notification.user_id == filters.user_id)
        if filters.processing_status:
            conditions.append(Notification.processing_status == filters.processing_status)
        if filters.category:
            conditions.append(Notification.category == filters.category)
        if filters.start_date:
            conditions.append(Notification.created_at >= filters.start_date)
        if filters.end_date:
            conditions.append(Notification.created_at <= filters.end_date)
        if filters.read is not None:
            conditions.append(Notification.read_at.isnot(None) if filters.read else Notification.read_at.is_(None))
        if filters.confidence is not None:
            conditions.append(Notification.confidence >= filters.confidence)

        if conditions:
            stmt = stmt.where(*conditions)

        stmt = stmt.offset(filters.skip).limit(filters.limit)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        """
        Получение уведомления по его ID.

        :param notification_id: Идентификатор уведомления.
        :return: Уведомление, если найдено, иначе None.
        """
        result = await self.db.execute(select(Notification).filter(Notification.id == str(notification_id)))
        return result.scalars().first()

    async def update_read_status(self, notification_id: UUID) -> Optional[Notification]:
        """
        Обновление статуса "прочитано" для уведомления.

        :param notification_id: Идентификатор уведомления.
        :return: Обновленное уведомление, если оно было найдено, иначе None.
        """
        stmt = select(Notification).filter(Notification.id == str(notification_id))
        result = await self.db.execute(stmt)
        db_notification = result.scalars().one_or_none()

        if db_notification:
            db_notification.read_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(db_notification)
            return db_notification
        return None

    async def get_status(self, notification_id: UUID) -> Optional[str]:
        """
        Получение статуса обработки уведомления.

        :param notification_id: Идентификатор уведомления.
        :return: Статус обработки уведомления, если найдено, иначе None.
        """
        stmt = select(Notification).filter(Notification.id == str(notification_id))
        result = await self.db.execute(stmt)
        db_notification = result.scalars().one_or_none()
        if db_notification:
            return db_notification.processing_status
        return None
