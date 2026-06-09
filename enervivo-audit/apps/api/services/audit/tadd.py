"""PASSE 2 — désambiguïsation des TADD par jalon.

Branché dans l'engine APRÈS la classification fichier-par-fichier (passe 1) et
APRÈS la passe plans de masse, AVANT le matching. Symétrique de `plan_masse.py`,
mais avec la logique TADD (cf. `services/llm/prompts/tadd.py`) :

  - Le jalon est SOUVENT explicite dans le nom du TADD → on ne devine jamais.
  - Un seul TADD RETENU par jalon (départage version interne puis date) →
    réécrit en "TADD version {jalon}" (nom EXACT attendu par documents_v12.json).
  - Les TADD ÉCARTÉS (versions antérieures d'un jalon déjà attribué) →
    "Autre / Non identifié" (ne polluent pas le matching).
  - Les TADD NON CLASSÉS (aucun jalon dans le nom) → laissés tels quels (la
    classification passe 1 est conservée, on ne devine pas).

Contrat :
  - Entrée : la liste `classified` (dicts en mémoire), telle que produite par
    l'engine, où chaque TADD a `classified_type` ~ "TADD version ...".
  - Effet : réécrit `classified_type` en mémoire ET dans classified_documents.
  - Fail-open : toute erreur (LLM down, JSON cassé) laisse la passe 1 intacte.
    Jamais de régression — au pire les TADD restent classés comme en passe 1.
"""

from __future__ import annotations

import logging
import unicodedata
import uuid
from typing import Any

from services.llm import get_llm_provider
from services.llm.prompts.tadd import (
    TADD_JALONS,
    build_tadd_system_prompt,
    build_tadd_user_prompt,
)
from services.llm.type_snap import OTHER_TYPE, TADD_UNCLASSIFIED_TYPE

log = logging.getLogger(__name__)


def _normalize(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s or "")
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_str.lower().split())


def _is_tadd(classified_type: str | None) -> bool:
    """Vrai si le type (passe 1) désigne un TADD, quel que soit le jalon.

    Couvre "TADD", "TADD version J1", "TADD J2a", etc.
    """
    if not classified_type:
        return False
    return _normalize(classified_type).startswith("tadd")


def _expected_name_for(jalon: str) -> str:
    """Nom EXACT attendu par le référentiel V13 pour un jalon donné."""
    return f"TADD version {jalon}"


async def reassign_tadd(
    classified: list[dict[str, Any]],
    audit_id: uuid.UUID,
) -> int:
    """Réassigne les TADD par jalon via un unique appel LLM.

    Retourne le nombre de TADD modifiés (retenus + écartés ; 0 si aucun TADD ou
    fail-open). Modifie `classified` en place et met à jour la DB.
    """
    # 1) Repérer les TADD (par leur position dans `classified`).
    tadd_indices = [
        i
        for i, c in enumerate(classified)
        # On ne touche pas aux fichiers en erreur d'extraction.
        if c.get("status_extraction") != "error" and _is_tadd(c.get("classified_type"))
    ]
    if not tadd_indices:
        return 0

    log.info("Passe 2 TADD : %d fichier(s) à départager", len(tadd_indices))

    # 2) Construire le listing pour le LLM (index LOCAL 0..N-1 → index global).
    local_to_global = {local: glob for local, glob in enumerate(tadd_indices)}
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
    # ⚠️ max_tokens : même raisonnement que plans de masse — on renvoie ~1 objet
    # JSON par TADD (retenu) + des index (écartés/non classés). On dimensionne
    # selon le nombre de TADD, avec marge et plancher, pour éviter une troncature
    # → JSONDecodeError → fail-open.
    max_tokens = max(600, 200 + 120 * len(tadd_indices))
    try:
        provider = get_llm_provider()
        system = build_tadd_system_prompt()
        user = build_tadd_user_prompt(files_payload)
        raw = await provider.complete_json(system, user, max_tokens=max_tokens)
    except Exception as e:  # fail-open
        log.warning("Passe 2 TADD : appel LLM KO (%s) — passe 1 conservée", e)
        return 0

    if not isinstance(raw, dict):
        log.warning("Passe 2 TADD : réponse LLM non-objet — passe 1 conservée")
        return 0

    selected = raw.get("selected")
    ecartes = raw.get("ecartes")
    non_classes = raw.get("non_classes")
    if not isinstance(selected, list):
        log.warning("Passe 2 TADD : réponse LLM sans 'selected' valide — passe 1 conservée")
        return 0

    # 4) Appliquer les ré-assignations valides (en mémoire + DB).
    valid_jalons = set(TADD_JALONS)
    updates: dict[str, str] = {}  # sharepoint_path → nouveau type (pour la DB)
    changed = 0
    # Un seul TADD retenu par jalon : on garde la première assignation valide et
    # on ignore les doublons éventuels (le LLM ne devrait pas en produire).
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
            # Doublon de jalon : on bascule ce candidat en écarté plus bas.
            continue
        jalon_pris.add(jalon)

        glob = local_to_global[local]
        c = classified[glob]
        new_type = _expected_name_for(jalon)
        c["classified_type"] = new_type
        # On enrichit la raison pour traçabilité dans le rapport.
        reason = str(a.get("reason", "")).strip()
        if reason:
            c["reason"] = f"[TADD → {jalon}] {reason}"
        updates[c["file"].path] = new_type
        changed += 1

    # Écartés : versions antérieures d'un jalon déjà attribué → "Autre".
    # ⚠️ GARDE-FOU : on n'écarte un TADD QUE si son jalon a effectivement un
    # fichier RETENU (jalon ∈ jalon_pris). Sans ce contrôle, un LLM qui range à
    # tort des TADD sans jalon dans "ecartes" (au lieu de "non_classes") les
    # ferait tous basculer en "Autre" alors qu'aucune version officielle n'a été
    # désignée — pire que la passe 1. Un "écarté" n'a de sens que face à un
    # "retenu" du même jalon.
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
            # Conditions cumulatives pour déclasser :
            #   - index connu et pas déjà retenu (sécurité)
            #   - jalon valide ET un fichier a bien été retenu pour ce jalon
            if local not in local_to_global or local in selected_locals:
                continue
            if jalon not in valid_jalons or jalon not in jalon_pris:
                # Incohérent (pas de retenu pour ce jalon) → on ne touche pas.
                continue
            glob = local_to_global[local]
            c = classified[glob]
            c["classified_type"] = OTHER_TYPE
            c["reason"] = f"[TADD écarté] version antérieure de {jalon} (déjà attribué)"
            updates[c["file"].path] = OTHER_TYPE
            changed += 1

    # "non_classes" : aucun token de jalon dans le nom. L'annexe TADD impose
    # « Non classé, exclu de la sélection, ne pas deviner » → type NEUTRE dédié
    # "TADD (non classé)" (≠ "Autre" : on garde l'étiquette TADD pour le voir
    # comme tel, hors-sélection). Ce libellé est protégé contre snap_type_to_
    # referential (cf. type_snap._PROTECTED_TYPES) pour survivre aux cache-hits.
    # Sans ça ils resteraient à la classif passe 1 (souvent "TADD version J1"
    # deviné) et compteraient à tort comme une version J1 officielle. Sécurité :
    # un index aussi présent dans selected (incohérence LLM) n'est PAS déclassé.
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
            # Idempotent : déjà posé (ex. via ecartes plus haut) → on saute.
            if c["classified_type"] in (OTHER_TYPE, TADD_UNCLASSIFIED_TYPE):
                continue
            c["classified_type"] = TADD_UNCLASSIFIED_TYPE
            c["reason"] = "[TADD non classé] aucun jalon dans le nom — exclu de la sélection"
            updates[c["file"].path] = TADD_UNCLASSIFIED_TYPE
            changed += 1

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
            log.warning("Passe 2 TADD : persist DB KO (%s) — rapport en mémoire OK quand même", e)

    log.info("Passe 2 TADD : %d/%d modifiés (retenus + écartés)", changed, len(tadd_indices))
    return changed
