"""Repository classifications — cache cross-audit par hash."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ClassifiedDocument


async def find_by_hash(session: AsyncSession, file_hash: str) -> ClassifiedDocument | None:
    """Cherche un document déjà classifié avec ce hash (économie LLM 100%).

    Un même hash peut avoir PLUSIEURS entrées (une par audit l'ayant classé),
    parfois avec des types différents (référentiel ou prompt ayant évolué entre
    deux audits). Sans tri, `LIMIT 1` renvoyait une ligne arbitraire → cache
    non-déterministe d'un audit à l'autre. On renvoie désormais la classification
    la PLUS RÉCENTE (`classified_at DESC`), qui reflète la dernière connaissance.
    """
    res = await session.execute(
        select(ClassifiedDocument)
        .where(ClassifiedDocument.file_hash == file_hash)
        .where(ClassifiedDocument.classified_type.is_not(None))
        .order_by(ClassifiedDocument.classified_at.desc())
        .limit(1)
    )
    return res.scalar_one_or_none()


async def create(session: AsyncSession, **kwargs) -> ClassifiedDocument:
    doc = ClassifiedDocument(**kwargs)
    session.add(doc)
    return doc
