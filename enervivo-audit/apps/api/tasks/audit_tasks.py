"""Tâches Celery — exécution audits (single ou en masse)."""

from __future__ import annotations

import asyncio
import logging
import uuid

from celery_app import celery_app

log = logging.getLogger(__name__)


@celery_app.task(name="tasks.audit.run_audit", bind=True, max_retries=2)
def run_audit_task(self, audit_id: str) -> None:
    """Wrapper sync → asyncio.run sur le moteur."""
    from services.audit.engine import run_audit

    try:
        asyncio.run(run_audit(uuid.UUID(audit_id)))
    except Exception as exc:
        log.exception("run_audit_task failure")
        raise self.retry(exc=exc, countdown=30) from exc


@celery_app.task(name="tasks.audit.mass_audit")
def mass_audit_task(audit_type: str = "juridique") -> dict:
    """Audit en masse — déclenche un audit pour chaque projet actif."""
    import asyncio as _asyncio

    from sqlalchemy import select

    from db.models import Audit, Project
    from db.session import AsyncSessionLocal

    async def _run() -> list[str]:
        ids: list[str] = []
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(Project))
            projects = list(res.scalars().all())
            for p in projects:
                audit = Audit(
                    project_code=p.code,
                    audit_type=audit_type,
                    jalons=[],
                    status="pending",
                )
                session.add(audit)
                await session.flush()
                ids.append(str(audit.id))
            await session.commit()
        return ids

    audit_ids = _asyncio.run(_run())
    for aid in audit_ids:
        run_audit_task.delay(aid)
    return {"triggered": len(audit_ids), "audit_ids": audit_ids}
