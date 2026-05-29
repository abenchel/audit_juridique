"""Interface des handlers d'audit."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AuditTypeHandler(ABC):
    @property
    @abstractmethod
    def audit_type(self) -> str: ...

    @abstractmethod
    def load_reference(self) -> dict[str, Any]:
        """Charge le référentiel (documents attendus)."""
        raise NotImplementedError

    def expected_for_jalons(self, reference: dict[str, Any], jalons: list[str]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for j in reference.get("jalons", []):
            if j["jalon"] in jalons:
                for doc in j["documents"]:
                    doc_copy = dict(doc)
                    doc_copy["_jalon"] = j["jalon"]
                    out.append(doc_copy)
        return out
