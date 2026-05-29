"""Setup auto du bucket cache PDF — exécuté au démarrage de l'API.

Idempotent : crée le bucket s'il n'existe pas, applique la lifecycle policy
(rétention {MINIO_RETENTION_DAYS} jours). Le quota disque MinIO se configure
au niveau du serveur via les variables d'env / la console (cf. doc).
"""

from __future__ import annotations

import asyncio
import logging

from minio.lifecycleconfig import Expiration, LifecycleConfig, Rule

from config.settings import get_settings

from .minio_client import get_minio_client

log = logging.getLogger(__name__)


def _setup_sync() -> None:
    s = get_settings()
    client = get_minio_client()

    # 1. Créer le bucket s'il n'existe pas
    if not client.bucket_exists(s.minio_bucket):
        client.make_bucket(s.minio_bucket)
        log.info("MinIO bucket créé : %s", s.minio_bucket)

    # 2. Appliquer la lifecycle policy (rétention auto)
    lifecycle = LifecycleConfig(
        [
            Rule(
                rule_id="auto-expire-pdf-cache",
                rule_filter=None,
                status="Enabled",
                expiration=Expiration(days=s.minio_retention_days),
            )
        ]
    )
    try:
        client.set_bucket_lifecycle(s.minio_bucket, lifecycle)
        log.info("MinIO lifecycle : objets supprimés après %d jours", s.minio_retention_days)
    except Exception as e:  # pragma: no cover
        log.warning("MinIO lifecycle setup échec : %s", e)


async def setup_lifecycle() -> None:
    """Au démarrage de l'API — async wrapper pour ne pas bloquer."""
    try:
        await asyncio.to_thread(_setup_sync)
    except Exception as e:
        log.warning("MinIO non disponible au démarrage (%s) — réessai au premier usage", e)
