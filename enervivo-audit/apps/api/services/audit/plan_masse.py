"""PASSE 2 — désambiguïsation des plans de masse par jalon.

Branché dans l'engine APRÈS la classification fichier-par-fichier (passe 1) et
AVANT le matching. Voir `services/llm/prompts/plan_masse.py` pour le pourquoi.

Contrat :
  - Entrée : la liste `classified` (dicts en mémoire), telle que produite par
    l'engine, où chaque plan de masse a `classified_type` ~ "Plan de masse...".
  - Effet : réécrit `classified_type` de chaque plan en
    "Plan de masse version {jalon}" (le nom EXACT attendu par documents_v12.json),
    en mémoire ET dans la table classified_documents (cohérence rebuild partiel).
  - Fail-open : toute erreur (LLM down, JSON cassé) laisse la passe 1 intacte.
    Jamais de régression — au pire les plans restent classés comme en passe 1.
"""

from __future__ import annotations

import logging
import unicodedata
import uuid
from typing import Any

from services.llm import get_llm_provider
from services.llm.prompts.plan_masse import (
    PLAN_MASSE_JALONS,
    build_plan_masse_system_prompt,
    build_plan_masse_user_prompt,
)

log = logging.getLogger(__name__)


def _normalize(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s or "")
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_str.lower().split())


def _is_plan_de_masse(classified_type: str | None) -> bool:
    """Vrai si le type (passe 1) désigne un plan de masse, quel que soit le jalon.

    Couvre "Plan de masse", "Plan de masse version J1", "Plan de Masse APS", etc.
    """
    if not classified_type:
        return False
    return _normalize(classified_type).startswith("plan de masse")


def _expected_name_for(jalon: str) -> str:
    """Nom EXACT attendu par le référentiel V12 pour un jalon donné."""
    return f"Plan de masse version {jalon}"


async def reassign_plans_de_masse(
    classified: list[dict[str, Any]],
    audit_id: uuid.UUID,
) -> int:
    """Réassigne les plans de masse par jalon via un unique appel LLM.

    Retourne le nombre de plans ré-assignés (0 si aucun plan, ou si fail-open).
    Modifie `classified` en place et met à jour la DB.
    """
    # 1) Repérer les plans de masse (par leur position dans `classified`).
    plan_indices = [
        i
        for i, c in enumerate(classified)
        # On ne touche pas aux fichiers en erreur d'extraction.
        if c.get("status_extraction") != "error"
        and _is_plan_de_masse(c.get("classified_type"))
    ]
    if not plan_indices:
        return 0

    log.info("Passe 2 plans de masse : %d fichier(s) à répartir", len(plan_indices))

    # 2) Construire le listing pour le LLM (index LOCAL 0..N-1 → index global).
    local_to_global = {local: glob for local, glob in enumerate(plan_indices)}
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
                # dossier parent = path sans le nom de fichier
                "folder": (f.path or "").rsplit("/", 1)[0] or "(racine)",
            }
        )

    # 3) Un seul appel LLM (texte) avec prompt système dédié.
    try:
        provider = get_llm_provider()
        system = build_plan_masse_system_prompt()
        user = build_plan_masse_user_prompt(files_payload)
        raw = await provider.complete_json(system, user)
    except Exception as e:  # fail-open
        log.warning("Passe 2 plans de masse : appel LLM KO (%s) — passe 1 conservée", e)
        return 0

    assignments = raw.get("assignments") if isinstance(raw, dict) else None
    if not isinstance(assignments, list):
        log.warning("Passe 2 : réponse LLM sans 'assignments' valide — passe 1 conservée")
        return 0

    # 4) Appliquer les ré-assignations valides (en mémoire + DB).
    valid_jalons = set(PLAN_MASSE_JALONS)
    updates: dict[str, str] = {}  # sharepoint_path → nouveau type (pour la DB)
    reassigned = 0

    for a in assignments:
        if not isinstance(a, dict):
            continue
        try:
            local = int(a.get("index"))
        except (TypeError, ValueError):
            continue
        jalon = str(a.get("jalon", "")).strip()
        if local not in local_to_global or jalon not in valid_jalons:
            continue

        glob = local_to_global[local]
        c = classified[glob]
        new_type = _expected_name_for(jalon)
        c["classified_type"] = new_type
        # On enrichit la raison pour traçabilité dans le rapport.
        pm_reason = str(a.get("reason", "")).strip()
        if pm_reason:
            c["reason"] = f"[Plan de masse → {jalon}] {pm_reason}"
        updates[c["file"].path] = new_type
        reassigned += 1

    # 5) Persister en DB pour que _rebuild_partial_report reste cohérent.
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
            log.warning("Passe 2 : persist DB KO (%s) — rapport en mémoire OK quand même", e)

    log.info("Passe 2 plans de masse : %d/%d ré-assignés", reassigned, len(plan_indices))
    return reassigned
