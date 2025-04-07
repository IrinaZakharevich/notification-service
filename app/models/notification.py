import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import Column, String


class Notification(Base):
    """
    Модель для хранения уведомлений.

    Эта модель представляет собой уведомления, которые могут быть отправлены пользователю. Она хранит информацию о пользователе,
    тексте уведомления, статусе, времени создания и времени прочтения.

    Атрибуты:
        id (UUID): Уникальный идентификатор уведомления (первичный ключ).
        user_id (UUID): Идентификатор пользователя, которому предназначено уведомление.
        title (str): Заголовок уведомления.
        text (str): Текст уведомления.
        created_at (datetime): Время создания уведомления (по умолчанию текущая дата и время).
        read_at (datetime): Время прочтения уведомления (может быть пустым).
        category (str): Категория уведомления (необязательный параметр).
        confidence (float): Уровень уверенности в классификации уведомления (необязательный параметр).
        processing_status (str): Статус обработки уведомления (по умолчанию "pending").
    """
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    read_at = Column(DateTime, nullable=True)

    category = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    processing_status = Column(String, default="pending", nullable=False)
