"""Types d'audit — un fichier par type."""

from __future__ import annotations

from .base import AuditTypeHandler
from .juridique import JuridiqueAudit


def get_handler(audit_type: str) -> AuditTypeHandler:
    if audit_type == "juridique":
        return JuridiqueAudit()
    raise NotImplementedError(f"Audit '{audit_type}' : v2")
