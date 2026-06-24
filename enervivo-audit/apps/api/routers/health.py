"""Health check + version endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from services.version import current_version

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "enervivo-audit-api"}


@router.get("/version")
async def version() -> dict[str, str | None]:
    """Version courante de l'outil (config/tool_version.json). Public."""
    return {"version": current_version()}
