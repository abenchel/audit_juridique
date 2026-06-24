"""Repository classifications — cache cross-audit par hash."""

from __future__ import annotations

import uuid

from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import array_agg
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Audit, ClassifiedDocument


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


async def purge_for_project(session: AsyncSession, project_code: str) -> int:
    """Supprime toutes les classifications des audits d'UN projet (relance
    « + nettoyer le cache »).

    Portée volontairement limitée au projet (via les audits du projet) : on ne
    touche JAMAIS les classifications d'autres projets, même si un fichier
    identique (même hash) y est partagé. La re-classification fraîche est
    garantie côté engine par `purge_cache=True` (bypass de `find_by_hash`).
    Ne commit pas (laissé à l'appelant).
    """
    res = await session.execute(
        delete(ClassifiedDocument).where(
            ClassifiedDocument.audit_id.in_(
                select(Audit.id).where(Audit.project_code == project_code)
            )
        )
    )
    return res.rowcount or 0


async def tool_versions_by_audit(
    session: AsyncSession, audit_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[str | None]]:
    """{audit_id -> [tool_version distinctes de ses classifications]}.

    Une seule requête agrégée (array_agg) pour éviter le N+1 lors du listing
    d'historique. Sert à calculer la « version du cache » (oldest_version) par audit.
    """
    if not audit_ids:
        return {}
    res = await session.execute(
        select(
            ClassifiedDocument.audit_id,
            array_agg(func.distinct(ClassifiedDocument.tool_version)),
        )
        .where(ClassifiedDocument.audit_id.in_(audit_ids))
        .group_by(ClassifiedDocument.audit_id)
    )
    return {row[0]: list(row[1] or []) for row in res.all()}
