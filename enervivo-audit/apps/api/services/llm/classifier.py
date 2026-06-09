"""Classifier — appel LLM avec prompt audit + parsing résultat."""

from __future__ import annotations

import logging
from typing import Any

from models.document import ClassificationResult

from . import get_llm_provider
from .prompts.juridique import build_system_prompt as build_juridique_system
from .prompts.juridique import build_user_prompt as build_juridique_user
from .prompts.juridique import build_user_prompt_vision as build_juridique_user_vision
from .type_snap import snap_type_to_referential

log = logging.getLogger(__name__)

# Cache prompt système par référentiel (évite reconstruction à chaque doc)
_SYSTEM_CACHE: dict[str, str] = {}


def _get_system_prompt(audit_type: str, documents_v11: dict[str, Any]) -> str:
    cache_key = f"{audit_type}:{documents_v11.get('version', 'unknown')}"
    if cache_key in _SYSTEM_CACHE:
        return _SYSTEM_CACHE[cache_key]
    if audit_type == "juridique":
        prompt = build_juridique_system(documents_v11)
    else:
        raise NotImplementedError(f"Type d'audit non supporté : {audit_type}")
    _SYSTEM_CACHE[cache_key] = prompt
    return prompt


async def classify(
    file_name: str,
    text_sample: str,
    audit_type: str,
    documents_v11: dict[str, Any],
    file_path: str | None = None,
) -> tuple[ClassificationResult, str]:
    """Retourne (résultat, nom_du_modèle).

    `file_path` (optionnel) : chemin SharePoint complet du fichier, transmis
    au LLM pour qu'il puisse comparer avec les "dossier" hints du référentiel
    V2 dans le system prompt (ex. un fichier dans /10-Raccordement n'est pas
    une LOI même si le contenu mentionne "engagement").
    """
    system_prompt = _get_system_prompt(audit_type, documents_v11)
    user_prompt = build_juridique_user(file_name, text_sample, file_path=file_path)
    provider = get_llm_provider()

    try:
        raw = await provider.complete_json(system_prompt, user_prompt)
    except Exception as e:
        log.exception("Échec LLM pour %s : %s", file_name, e)
        raise

    # Validation / coercion
    type_value = str(raw.get("type", "Autre / Non identifié")).strip() or "Autre / Non identifié"
    # Garde-fou : ramène un type inventé hors-référentiel V12 vers un type valide
    # (alias métier / snap au plus proche / sinon Autre). `documents_v11` = nom de
    # variable historique mais contient bien le V12. Cf. type_snap.py.
    type_value = snap_type_to_referential(type_value, documents_v11)
    try:
        conf = int(raw.get("confidence", 0))
    except (TypeError, ValueError):
        conf = 0
    conf = max(0, min(100, conf))
    reason = str(raw.get("reason", "")).strip()[:300]

    return (
        ClassificationResult(type=type_value, confidence=conf, reason=reason),
        provider.model_name,
    )


async def classify_vision(
    file_name: str,
    images: list[bytes] | list[tuple[bytes, str]],
    audit_type: str,
    documents_v11: dict[str, Any],
    file_path: str | None = None,
    ocr_text: str | None = None,
) -> tuple[ClassificationResult, str]:
    """Classification multimodale (vision LLM).

    Cas d'usage :
      - PDF scannés (sans couche texte) → images = pages rendues en PNG via pymupdf,
        + `ocr_text` = texte Tesseract de toutes les pages (complément du visuel)
      - Images natives (jpg/png/heic) → images = [(content, mime_type)] directement,
        `ocr_text` laissé à None (pas d'OCR sur les images natives)

    Mêmes contrats que `classify()` mais le sample texte est remplacé par
    les images (+ OCR optionnel). `images` accepte `list[bytes]` (PNG par
    défaut) ou `list[tuple[bytes, mime_type]]`.
    """
    system_prompt = _get_system_prompt(audit_type, documents_v11)
    user_prompt = build_juridique_user_vision(
        file_name, file_path=file_path, ocr_text=ocr_text
    )
    provider = get_llm_provider()

    try:
        raw = await provider.complete_json_vision(system_prompt, user_prompt, images)
    except Exception as e:
        log.exception("Échec LLM vision pour %s : %s", file_name, e)
        raise

    type_value = str(raw.get("type", "Autre / Non identifié")).strip() or "Autre / Non identifié"
    # Même garde-fou que classify() : snap vers le référentiel V12.
    type_value = snap_type_to_referential(type_value, documents_v11)
    try:
        conf = int(raw.get("confidence", 0))
    except (TypeError, ValueError):
        conf = 0
    conf = max(0, min(100, conf))
    reason = str(raw.get("reason", "")).strip()[:300]

    return (
        ClassificationResult(type=type_value, confidence=conf, reason=reason),
        provider.model_name + " [vision]",
    )
