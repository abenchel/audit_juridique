"""Client MinIO (S3-compatible) — sync sous le capot, wrappé via asyncio.to_thread."""

from __future__ import annotations

from functools import lru_cache

from minio import Minio

from config.settings import get_settings


@lru_cache(maxsize=1)
def get_minio_client() -> Minio:
    s = get_settings()
    return Minio(
        endpoint=s.minio_endpoint,
        access_key=s.minio_access_key,
        secret_key=s.minio_secret_key.get_secret_value(),
        secure=s.minio_secure,
    )
