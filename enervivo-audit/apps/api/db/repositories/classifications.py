"""Repository classifications — cache cross-audit par hash."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ClassifiedDocument


async def find_by_hash(session: AsyncSession, file_hash: str) -> ClassifiedDocument | None:
    """Cherche un document déjà classifié avec ce hash (économie LLM 100%)."""
    res = await session.execute(
        select(ClassifiedDocument)
        .where(ClassifiedDocument.file_hash == file_hash)
        .where(ClassifiedDocument.classified_type.is_not(None))
        .limit(1)
    )
    return res.scalar_one_or_none()


async def create(session: AsyncSession, **kwargs) -> ClassifiedDocument:
    doc = ClassifiedDocument(**kwargs)
    session.add(doc)
    return doc
