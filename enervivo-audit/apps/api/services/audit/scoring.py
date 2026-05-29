"""Scoring : seuils de confiance pour classer un document.

Cahier des charges §6.1 :
  - ≥ 70 % : Trouvé
  - 40-70 % : Ambigu (revue manuelle)
  - < 40 % : Manquant (faible confiance)
"""

from __future__ import annotations

from typing import Literal

from config.settings import get_settings

ConfidenceTier = Literal["present", "ambiguous", "missing"]


def tier(confidence: int) -> ConfidenceTier:
    s = get_settings()
    if confidence >= s.confidence_threshold_present:
        return "present"
    if confidence >= s.confidence_threshold_ambiguous:
        return "ambiguous"
    return "missing"
