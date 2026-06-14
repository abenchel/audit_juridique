"""PASSE 2 — désambiguïsation des dossiers de qualification par jalon.

Branché dans l'engine APRÈS la classification fichier-par-fichier (passe 1) et
APRÈS les passes plans de masse + TADD, AVANT le matching. Calqué sur `tadd.py`
(même logique « jalon dans le nom »), cf. `services/llm/prompts/qualification.py` :

  - Le jalon est déterminé UNIQUEMENT par un token dans le nom (.pptx/.ppt) →
    on ne devine jamais.
  - Un seul dossier RETENU par jalon (départage : date du nom puis date système)
    → réécrit en "Dossier de qualification {jalon}" (nom EXACT du référentiel V13).
  - Les dossiers ÉCARTÉS (versions antérieures d'un jalon déjà attribué) →
    "Autre / Non identifié" (ne polluent pas le matching).
  - Les dossiers NON CLASSÉS (aucun jalon dans le nom) → type neutre dédié
    "Dossier de qualification (non classé)" (protégé du snap), exclu de la sélection.

Fail-open : toute erreur (LLM down, JSON cassé) laisse la passe 1 intacte.
"""

from __future__ import annotations

import logging
import unicodedata
import uuid
from typing import Any

from services.llm import get_llm_provider
from services.llm.prompts.qualification import (
    QUALIF_JALONS,
    build_qualification_system_prompt,
    build_qualification_user_prompt,
)
from services.llm.type_snap import OTHER_TYPE, QUALIF_UNCLASSIFIED_TYPE

log = logging.getLogger(__name__)


def _normalize(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s or "")
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_str.lower().split())


def _is_qualification(classified_type: str | None) -> bool:
    """Vrai si le type (passe 1) désigne un dossier de qualification.

    Couvre "Dossier de qualification", "Dossier de qualification J1", etc.
    """
    if not classified_type:
        return False
    return _normalize(classified_type).startswith("dossier de qualification")


def _expected_name_for(jalon: str) -> str:
    """Nom EXACT attendu par le référentiel V13 pour un jalon donné."""
    return f"Dossier de qualification {jalon}"


async def reassign_qualification(
    classified: list[dict[str, Any]],
    audit_id: uuid.UUID,
) -> int:
    """Réassigne les dossiers de qualification par jalon via un unique appel LLM.

    Retourne le nombre de dossiers modifiés (retenus + écartés + non classés ; 0
    si aucun dossier ou fail-open). Modifie `classified` en place + met à jour la DB.
    """
    # 1) Repérer les dossiers de qualification (par position dans `classified`).
    qualif_indices = [
        i
        for i, c in enumerate(classified)
        if c.get("status_extraction") != "error"
        and _is_qualification(c.get("classified_type"))
    ]
    if not qualif_indices:
        return 0

    log.info("Passe 2 qualification : %d fichier(s) à départager", len(qualif_indices))

    # 2) Listing pour le LLM (index LOCAL 0..N-1 → index global).
    local_to_global = {local: glob for local, glob in enumerate(qualif_indices)}
    files_payload: list[dict[str, Any]] = []
    for local, glob in local_to_global.items():
        c = classified[glob]
        f = c["file"]
        modified = getattr(f, "modified_at", None)
        files_payload.append(
            {
                "index": local,
                "name": f.name,
                "modified_at": modified.isoformat() if modified else None,
                "folder": (f.path or "").rsplit("/", 1)[0] or "(racine)",
            }
        )

    # 3) Un seul appel LLM. max_tokens dimensionné (~1 objet/dossier) pour éviter
    # la troncature JSON → JSONDecodeError → fail-open.
    max_tokens = max(600, 200 + 120 * len(qualif_indices))
    try:
        provider = get_llm_provider()
        system = build_qualification_system_prompt()
        user = build_qualification_user_prompt(files_payload)
        raw = await provider.complete_json(system, user, max_tokens=max_tokens)
    except Exception as e:  # fail-open
        log.warning("Passe 2 qualification : appel LLM KO (%s) — passe 1 conservée", e)
        return 0

    if not isinstance(raw, dict):
        log.warning("Passe 2 qualification : réponse LLM non-objet — passe 1 conservée")
        return 0

    selected = raw.get("selected")
    ecartes = raw.get("ecartes")
    non_classes = raw.get("non_classes")
    if not isinstance(selected, list):
        log.warning(
            "Passe 2 qualification : réponse LLM sans 'selected' valide — passe 1 conservée"
        )
        return 0

    # 4) Appliquer les ré-assignations (mémoire + DB).
    valid_jalons = set(QUALIF_JALONS)
    updates: dict[str, str] = {}
    changed = 0
    jalon_pris: set[str] = set()

    for a in selected:
        if not isinstance(a, dict):
            continue
        try:
            local = int(a.get("index"))
        except (TypeError, ValueError):
            continue
        jalon = str(a.get("jalon", "")).strip()
        if local not in local_to_global or jalon not in valid_jalons:
            continue
        if jalon in jalon_pris:
            continue
        jalon_pris.add(jalon)

        glob = local_to_global[local]
        c = classified[glob]
        new_type = _expected_name_for(jalon)
        c["classified_type"] = new_type
        reason = str(a.get("reason", "")).strip()
        if reason:
            c["reason"] = f"[Qualification → {jalon}] {reason}"
        updates[c["file"].path] = new_type
        changed += 1

    # Écartés : versions antérieures d'un jalon déjà attribué → "Autre".
    # GARDE-FOU : on n'écarte QUE si le jalon a effectivement un fichier retenu
    # (jalon ∈ jalon_pris). Un "écarté" n'a de sens que face à un "retenu".
    selected_locals = {
        int(a["index"])
        for a in selected
        if isinstance(a, dict) and isinstance(a.get("index"), int)
    }
    if isinstance(ecartes, list):
        for x in ecartes:
            if not isinstance(x, dict):
                continue
            try:
                local = int(x.get("index"))
            except (TypeError, ValueError):
                continue
            jalon = str(x.get("jalon", "")).strip()
            if local not in local_to_global or local in selected_locals:
                continue
            if jalon not in valid_jalons or jalon not in jalon_pris:
                continue
            glob = local_to_global[local]
            c = classified[glob]
            c["classified_type"] = OTHER_TYPE
            c["reason"] = f"[Qualification écartée] version antérieure de {jalon} (déjà attribué)"
            updates[c["file"].path] = OTHER_TYPE
            changed += 1

    # Non classés : aucun token de jalon → type neutre dédié protégé du snap.
    if isinstance(non_classes, list):
        for x in non_classes:
            try:
                local = int(x)
            except (TypeError, ValueError):
                continue
            if local not in local_to_global or local in selected_locals:
                continue
            glob = local_to_global[local]
            c = classified[glob]
            if c["classified_type"] in (OTHER_TYPE, QUALIF_UNCLASSIFIED_TYPE):
                continue
            c["classified_type"] = QUALIF_UNCLASSIFIED_TYPE
            c["reason"] = (
                "[Qualification non classée] aucun jalon dans le nom — exclu de la sélection"
            )
            updates[c["file"].path] = QUALIF_UNCLASSIFIED_TYPE
            changed += 1

    # 5) Persister en DB pour cohérence avec _rebuild_partial_report.
    if updates:
        try:
            from sqlalchemy import update as sa_update

            from db.models import ClassifiedDocument
            from db.session import AsyncSessionLocal

            async with AsyncSessionLocal() as session:
                for path, new_type in updates.items():
                    await session.execute(
                        sa_update(ClassifiedDocument)
                        .where(
                            ClassifiedDocument.audit_id == audit_id,
                            ClassifiedDocument.sharepoint_path == path,
                        )
                        .values(classified_type=new_type)
                    )
                await session.commit()
        except Exception as e:  # fail-open : la mémoire est déjà correcte
            log.warning(
                "Passe 2 qualification : persist DB KO (%s) — rapport en mémoire OK quand même",
                e,
            )

    log.info(
        "Passe 2 qualification : %d/%d modifiés (retenus + écartés + non classés)",
        changed,
        len(qualif_indices),
    )
    return changed
