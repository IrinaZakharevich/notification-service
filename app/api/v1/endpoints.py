import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationStatus, NotificationFilter
from app.services.notification_services import NotificationService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/notifications/",
             response_model=NotificationRead,
             summary="Создание уведомления",
             description="Создает новое уведомление и запускает его асинхронную обработку.")
async def create_notification_endpoint(
        notification: NotificationCreate,
        db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    return await notification_service.create_notification(notification=notification)


@router.get("/notifications/",
            response_model=list[NotificationRead],
            summary="Получение уведомлений",
            description="""
            Возвращает список уведомлений с возможностью фильтрации по следующим параметрам:
            - user_id
            - processing_status
            - category
            - start_date, end_date
            - confidence

            Также поддерживаются параметры `skip` и `limit` для пагинации.
            """
            )
@cache(expire=10)
async def get_notifications_endpoint(
        filters: NotificationFilter = Depends(),
        db: AsyncSession = Depends(get_db)
):
    logger.info("Actual DB query executed")
    notification_service = NotificationService(db)
    return await notification_service.get_notifications(filters)


@router.get("/notifications/{notification_id}",
            response_model=NotificationRead,
            summary="Получение уведомления по id",
            description="Возвращает одно уведомление по его уникальному идентификатору.")
async def get_notification_by_id_endpoint(
        notification_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification = await notification_service.get_notification_by_id(notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.patch("/notifications/{notification_id}/read",
              response_model=NotificationRead,
              summary="Пометить уведомление как прочитанное",
              description="Помечает уведомление как прочитанное (устанавливает дату прочтения).")
async def mark_notification_as_read(
        notification_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    notification = await notification_service.update_read_status(notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.get("/notifications/{notification_id}/status",
            response_model=NotificationStatus,
            summary="Получить статус уведомления",
            description="Возвращает текущий статус обработки уведомления.")
async def get_notification_status_endpoint(
        notification_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    notification_service = NotificationService(db)
    status = await notification_service.get_notification_status(notification_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return status
