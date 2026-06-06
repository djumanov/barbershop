from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "barbershop",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.task_time_limit = settings.celery_task_timeout_seconds


@celery_app.task(name="ping")
def ping() -> str:
    """Trivial task to verify worker + broker + result backend wiring."""
    return "pong"
