# 📣 Notification Service

Микросервис для управления и обработки уведомлений, построенный на FastAPI, SQLAlchemy (async), Redis и Celery.
сервис уведомлений для интеграции с AI-моделями. Сервис предоставлят REST API на FastAPI и может интегрироваться с 
внешним AI API (здесь используется mock) для анализа содержимого уведомлений.

---

## 📦 Стек технологий

- **FastAPI** — основной web-фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy (async)** — ORM
- **Celery** — фоновые задачи
- **Redis** — брокер задач и кэш
- **Docker / Docker Compose** — контейнеризация
- **Pytest** — тестирование

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/IrinaZakharevich/notification-service.git
cd notification-service
```

## 🚀 Быстрый старт

### 2. Создай .env файл

```bash
cp .env.example .env
```

### 3. Построй и запусти контейнеры

```bash
docker-compose up --build
```

Приложение будет доступно по адресу:
👉 http://localhost:8080

📚 Основные эндпоинты

Метод Путь Описание

GET /v1/notifications/ Получить список уведомлений

POST /v1/notifications/ Создать новое уведомление

GET /v1/notifications/{id} Получить уведомление по ID

PATCH /v1/notifications/{id}/read Отметить уведомление как прочитанное

GET /v1/notifications/{id}/status Получить статус уведомления

GET /ping_db Проверить соединение с базой данных

Swagger-документация доступна по адресу:

👉 http://localhost:8080/docs

### 4. Запуск тестов

Чтобы запустить тесты в Docker:

```bash
docker exec -it web pytest tests
```
