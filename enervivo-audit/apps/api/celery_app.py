"""Celery entrypoint — worker + beat."""

from __future__ import annotations

from celery import Celery

from config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "enervivo_audit",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["tasks.audit_tasks", "tasks.sync_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Paris",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
    result_expires=3600 * 24 * 7,
)

# v2 : tâches planifiées (sync SharePoint, etc.)
celery_app.conf.beat_schedule = {}
