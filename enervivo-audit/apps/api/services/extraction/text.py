"""Extracteur texte brut — .txt / .xml et autres formats UTF-ish.

XML : on garde le texte tel quel (les balises portent du sens pour le LLM,
ex. <Signataire>, <DateDepot>). Pas de parsing strict — fail-safe sur encodage.
"""

from __future__ import annotations

from .base import ExtractionError, TextExtractor


class PlainTextExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                text = content.decode(enc)
                if text.strip():
                    return text
                raise ExtractionError("fichier texte vide")
            except UnicodeDecodeError:
                continue
        raise ExtractionError("encodage texte non détecté")
