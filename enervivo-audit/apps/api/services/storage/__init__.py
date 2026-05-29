"""Service stockage objet — MinIO S3-compatible."""

from __future__ import annotations

from .cache import PDFCache
from .lifecycle import setup_lifecycle
from .minio_client import get_minio_client

__all__ = ["PDFCache", "get_minio_client", "setup_lifecycle"]
