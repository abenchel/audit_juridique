"""Cache PDF par hash SHA-256.

Stratégie : on cache les BYTES bruts dans MinIO pour éviter de retélécharger
SharePoint si on relance l'audit. Le cache cross-audit par classification est
géré ailleurs (Postgres : ClassifiedDocument.file_hash → réutilise type/conf).

Cycle de vie : 30 jours via lifecycle policy. Quota 5Go.
"""

from __future__ import annotations

import asyncio
import io
import logging

from minio.error import S3Error

from config.settings import get_settings

from .minio_client import get_minio_client

log = logging.getLogger(__name__)


class PDFCache:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._client = get_minio_client()
        self._bucket = self._settings.minio_bucket

    def _key(self, file_hash: str) -> str:
        return f"{file_hash[:2]}/{file_hash}"  # sharding par préfixe

    async def get(self, file_hash: str) -> bytes | None:
        try:
            return await asyncio.to_thread(self._get_sync, file_hash)
        except S3Error as e:
            if e.code == "NoSuchKey":
                return None
            log.warning("PDFCache.get S3Error : %s", e)
            return None
        except Exception as e:  # pragma: no cover
            log.warning("PDFCache.get error : %s", e)
            return None

    def _get_sync(self, file_hash: str) -> bytes:
        resp = self._client.get_object(self._bucket, self._key(file_hash))
        try:
            return resp.read()
        finally:
            resp.close()
            resp.release_conn()

    async def put(self, file_hash: str, content: bytes, mime_type: str = "application/octet-stream") -> None:
        try:
            await asyncio.to_thread(self._put_sync, file_hash, content, mime_type)
        except Exception as e:  # pragma: no cover
            log.warning("PDFCache.put error : %s", e)

    def _put_sync(self, file_hash: str, content: bytes, mime_type: str) -> None:
        self._client.put_object(
            self._bucket,
            self._key(file_hash),
            io.BytesIO(content),
            length=len(content),
            content_type=mime_type,
        )
