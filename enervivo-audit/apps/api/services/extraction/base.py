"""Interface TextExtractor."""

from __future__ import annotations

from abc import ABC, abstractmethod

# Sample : 2000 premiers + 800 derniers caractères (optimisé pour vitesse + coût LLM)
# Ancien: 3000+1000 = 4000 chars = ~900 tokens → coûteux
# Nouveau: 2000+800 = 2800 chars = ~600 tokens (33% moins cher)
# Plus que suffisant pour identifier un doc juridique
HEAD_CHARS = 2000
TAIL_CHARS = 800


class TextExtractor(ABC):
    """Extrait du texte d'un blob binaire."""

    @abstractmethod
    def extract(self, content: bytes) -> str:
        """Retourne le texte brut. Lève ExtractionError si illisible."""
        raise NotImplementedError


class ExtractionError(Exception):
    """Échec d'extraction (fichier protégé, corrompu…)."""


class ScanNoTextError(ExtractionError):
    """Cas particulier : PDF valide mais sans couche texte (scan).

    Le pipeline peut alors fallback sur une classification basée sur le nom
    du fichier uniquement, plutôt que de marquer le document en erreur dure.
    """


def truncate_sample(text: str) -> str:
    """Renvoie head + … + tail, comme spécifié dans le cahier des charges."""
    text = text.strip()
    if len(text) <= HEAD_CHARS + TAIL_CHARS:
        return text
    return text[:HEAD_CHARS] + "\n\n[...]\n\n" + text[-TAIL_CHARS:]
