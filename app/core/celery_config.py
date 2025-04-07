import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "celery_config",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    include=["app.tasks.tasks"],
)

celery_app.conf.update(
    result_expires=3600,
)

celery_app.conf.update(task_routes={"app.tasks.tasks.analyze": {"queue": "celery"}})

celery_app.autodiscover_tasks(["app.tasks"])
