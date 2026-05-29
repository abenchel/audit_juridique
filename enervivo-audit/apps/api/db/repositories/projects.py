"""Repository projets — accès DB encapsulé."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Project


async def list_projects(session: AsyncSession) -> list[Project]:
    res = await session.execute(select(Project).order_by(Project.code))
    return list(res.scalars().all())


async def get_project(session: AsyncSession, code: str) -> Project | None:
    return await session.get(Project, code)


async def upsert_project(session: AsyncSession, data: dict) -> Project:
    existing = await session.get(Project, data["code"])
    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
        return existing
    project = Project(**data)
    session.add(project)
    return project
