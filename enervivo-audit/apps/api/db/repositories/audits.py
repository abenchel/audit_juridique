"""Repository audits."""

from __future__ import annotations

import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Audit


async def create_audit(session: AsyncSession, **kwargs) -> Audit:
    audit = Audit(**kwargs)
    session.add(audit)
    await session.flush()
    return audit


async def get_audit(session: AsyncSession, audit_id: uuid.UUID) -> Audit | None:
    return await session.get(Audit, audit_id)


async def list_audits_for_project(session: AsyncSession, project_code: str, limit: int = 20) -> list[Audit]:
    res = await session.execute(
        select(Audit).where(Audit.project_code == project_code).order_by(desc(Audit.started_at)).limit(limit)
    )
    return list(res.scalars().all())
