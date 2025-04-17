from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.users", "app.tasks.orders"]
)

celery_app.conf.task_routes = {
    "app.tasks.users.*": {"queue": "users"},
    "app.tasks.orders.*": {"queue": "orders"}
}

celery_app.conf.beat_schedule = {
    "clean-unverified-users": {
        "task": "app.tasks.users.clean_unverified_users",
        "schedule": crontab(minute=0, hour=0),  # Run at midnight every day
    },
}
