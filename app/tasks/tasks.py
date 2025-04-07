import asyncio
import logging

from app.ai.mock_service import analyze_text
from app.models.notification import Notification
from app.core.celery_config import celery_app
from app.core.database import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@celery_app.task(name="app.tasks.tasks.analyze")
def analyze(notification_id: str):
    """
    Задача Celery для анализа уведомления.

    Эта задача инициирует асинхронную обработку уведомления по его идентификатору.
    Выполняется в фоновом режиме с использованием Celery.

    :param notification_id: Идентификатор уведомления, которое нужно проанализировать.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process(notification_id))


async def process(notification_id: str):
    """
    Асинхронный процесс для обработки уведомления.

    Обновляет статус уведомления в базе данных, запускает анализ текста уведомления,
    и сохраняет результаты (категорию и уверенность) обратно в уведомление.

    :param notification_id: Идентификатор уведомления, которое нужно обработать.
    """
    async with AsyncSessionLocal() as session:
        try:
            notification_id = str(notification_id)
            notification = await session.get(Notification, notification_id)

            if notification:
                notification.processing_status = "processing"
                await session.commit()
                await session.refresh(notification)
                results = await analyze_text(notification.text)
                notification.category = results["category"]
                notification.confidence = results["confidence"]
                notification.processing_status = "completed"
                await session.commit()
                await session.refresh(notification)
            else:
                logger.warning(f"Notification with id {notification_id} not found.")
        except Exception as e:
            result = await session.get(Notification, notification_id)
            notification = result.scalars().first()
            logger.info(notification)
            notification.processing_status = "failed"
            await session.commit()
            raise e
