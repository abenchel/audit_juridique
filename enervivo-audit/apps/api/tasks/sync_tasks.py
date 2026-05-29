"""Tâches Celery synchronisation (v2 — sync SharePoint → BDD projets)."""

from __future__ import annotations

from celery_app import celery_app


@celery_app.task(name="tasks.sync.sharepoint_projects")
def sync_sharepoint_projects() -> dict:  # pragma: no cover
    # v2 : récupère liste des projets depuis SharePoint et upsert dans Postgres
    return {"status": "v2 — non implémenté"}
