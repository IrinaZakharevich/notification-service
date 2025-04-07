import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    """
    Схема для создания уведомления.
    """
    user_id: uuid.UUID
    title: str = Field(..., min_length=3, max_length=50)
    text: str = Field(..., min_length=5, max_length=500)


class NotificationResponse(BaseModel):
    """
    Схема для ответа с данными уведомления.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    text: str
    created_at: datetime
    read_at: Optional[datetime] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    processing_status: str

    model_config = {"from_attributes": True}


class NotificationRead(BaseModel):
    """
    Схема для чтения данных уведомления.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    text: str
    created_at: datetime
    read_at: Optional[datetime] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    processing_status: str

    model_config = {"from_attributes": True}


class NotificationStatus(BaseModel):
    """
    Схема для отображения статуса уведомления.
    """
    processing_status: str


class NotificationFilter(BaseModel):
    """
    Схема для фильтрации уведомлений.

    Эта схема используется для фильтрации уведомлений по различным параметрам, таким как пользователь, статус, дата и другие.

    Атрибуты:
        skip (int): Количество пропущенных записей (для пагинации).
        limit (int): Максимальное количество уведомлений, которые следует вернуть.
        user_id (Optional[str]): Идентификатор пользователя для фильтрации.
        processing_status (Optional[str]): Статус обработки уведомлений.
        category (Optional[str]): Категория уведомлений.
        start_date (Optional[datetime]): Начальная дата для фильтрации по времени.
        end_date (Optional[datetime]): Конечная дата для фильтрации по времени.
        read (Optional[bool]): Фильтрация по состоянию прочтения уведомлений.
        confidence (Optional[float]): Минимальный уровень уверенности для фильтрации уведомлений.
    """
    skip: int = 0
    limit: int = 100
    user_id: Optional[str] = None
    processing_status: Optional[str] = None
    category: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    read: Optional[bool] = None
    confidence: Optional[float] = None
