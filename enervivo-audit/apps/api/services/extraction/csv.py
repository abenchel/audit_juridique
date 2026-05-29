"""Extraction CSV — décode en texte avec auto-détection encoding.

Rarement juridique (plus souvent données techniques type TMY météo, profils
de consommation), mais on supporte au cas où — le LLM classera en
"Autre / Non identifié" si pas pertinent.
"""

from __future__ import annotations

from .base import HEAD_CHARS, ExtractionError, TextExtractor

_HEAD_BUDGET = HEAD_CHARS * 2


class CsvExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                text = content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ExtractionError("CSV : encoding non détecté")

        if not text.strip():
            raise ExtractionError("CSV vide")
        return text[:_HEAD_BUDGET]
