"""Router admin — réservé aux administrateurs (users.role == 'admin').

Le contrôle d'accès s'appuie sur `require_admin`, qui lit le rôle RÉEL depuis la
DB (cf. services/auth/deps.py). Un non-admin reçoit 403.
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from services.auth.deps import require_admin
from services.auth.jwt_verify import TokenPayload
from services.version import full_changelog

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/changelog")
async def get_changelog(
    _admin: Annotated[TokenPayload, Depends(require_admin)],
) -> list[dict[str, Any]]:
    """Changelog complet de l'outil (versions V1, V2… avec date + description).

    Visible admin uniquement. Source : config/tool_version.json.
    """
    return full_changelog()
