"""Audit technique — stub v2."""

from __future__ import annotations

from .base import AuditTypeHandler


class TechniqueAudit(AuditTypeHandler):  # pragma: no cover
    @property
    def audit_type(self) -> str:
        return "technique"

    def load_reference(self) -> dict:
        raise NotImplementedError("Audit technique : v2")
