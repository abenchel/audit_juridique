"""Tâches Celery — exécution audits (single ou en masse)."""

from __future__ import annotations

import asyncio
import logging
import uuid
from collections.abc import Awaitable, Callable
from typing import TypeVar

from celery_app import celery_app

log = logging.getLogger(__name__)

_T = TypeVar("_T")


def _run_in_fresh_loop(coro_factory: Callable[[], Awaitable[_T]]) -> _T:
    """Exécute une coroutine dans un nouveau loop, avec un pool DB propre.

    ⚠️ Celery exécute chaque tâche via `asyncio.run()` = NOUVEL event loop à
    chaque fois. Or l'engine SQLAlchemy async (`db.session.engine`) est créé
    une fois au niveau module et garde un pool de connexions asyncpg liées au
    loop de la PREMIÈRE tâche. À la 2ᵉ tâche, le pool tente de réutiliser une
    connexion de l'ancien loop (fermé) → `got Future attached to a different
    loop` / `Event loop is closed`.

    Fix : on `dispose()` l'engine DANS le nouveau loop (purge le pool ; SQLAlchemy
    le recrée à la demande avec des connexions liées au loop courant) avant ET
    après l'exécution. `dispose()` est idempotent et async-safe.
    """

    async def _wrapped() -> _T:
        from db.session import engine

        await engine.dispose()  # purge les connexions de l'ancien loop
        try:
            return await coro_factory()
        finally:
            await engine.dispose()  # libère ce loop avant fermeture

    return asyncio.run(_wrapped())


@celery_app.task(name="tasks.audit.run_audit", bind=True, max_retries=2)
def run_audit_task(self, audit_id: str) -> None:
    """Wrapper sync → asyncio.run sur le moteur (pool DB recréé par tâche)."""
    from services.audit.engine import run_audit

    try:
        _run_in_fresh_loop(lambda: run_audit(uuid.UUID(audit_id)))
    except Exception as exc:
        log.exception("run_audit_task failure")
        raise self.retry(exc=exc, countdown=30) from exc


@celery_app.task(name="tasks.audit.mass_audit")
def mass_audit_task(audit_type: str = "juridique") -> dict:
    """Audit en masse — déclenche un audit pour chaque projet actif."""
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

    audit_ids = _run_in_fresh_loop(_run)
    for aid in audit_ids:
        run_audit_task.delay(aid)
    return {"triggered": len(audit_ids), "audit_ids": audit_ids}
