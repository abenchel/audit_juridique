"""Matcher : associe documents classifiés ↔ référentiel V11 attendu.

Algorithme :
  1. Pour chaque attendu d'un jalon, on cherche tous les classifiés dont le
     'classified_type' correspond exactement au 'name' du référentiel.
  2. Pour chaque match, on applique le scoring (present / ambiguous / missing).
  3. Plusieurs fichiers peuvent matcher (ex. 3 CR RDV maire) — tous listés.
  4. Si aucun → statut 'missing' sauf si 'propriete' rend non applicable.

Cas spéciaux (cahier des charges §6.2) :
  - propriete = 'Cas par cas' (V12, 23/107 docs) : doc conditionnellement
    applicable selon la situation du projet (ex. EPA, ICPE, contrats > 5 MWc,
    test d'arrachement). Si non trouvé → 'not_applicable' par défaut — l'UI
    affiche la `note` métier pour que le BE juge si le doc est vraiment dû.
    Évite les faux positifs « missing » massifs sur des docs facultatifs par
    construction.
  - 'Attestation MSA' (Annexes 3 PDB) : non applicable si projet ≠ AgriPV.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import unicodedata

from models.audit import ExpectedDocument, FoundFile
from models.document import FileMetadata

from .scoring import tier


_DASH_VARIANTS = {
    "‐", "‑", "‒", "–", "—", "―",  # ‐ ‑ ‒ – — ―
    "−",  # math minus
    "­",  # soft hyphen
}


def _normalize_type(s: str) -> str:
    """Normalisation tolérante : sans accents, minuscule, espaces compactés.

    Aussi : toutes les variantes de tirets (em-dash, en-dash, etc.) ramenées à un
    espace, pour éviter que 'DT — DT résumé' (LLM, em-dash U+2014) ne matche pas
    'DT - DT résumé' (V12, hyphen-minus U+002D).
    """
    for d in _DASH_VARIANTS:
        s = s.replace(d, "-")
    s = s.replace("-", " ")
    nfkd = unicodedata.normalize("NFKD", s)
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_str.lower().split())


def _find_prefix_match(
    classified_key: str,
    expected_keys: list[str],
) -> str | None:
    """Fallback : si le LLM a tronqué le nom (ex. 'Relevé d'identité bancaire (RIB)'
    au lieu de 'Relevé d'identité bancaire (RIB) pour versement redevances...'),
    on accepte un préfixe UNIQUE. Retourne la clé normalisée de l'expected
    si exactement UN expected commence par classified_key + ' ' (ou inversement
    classified_key commence par un expected unique). Sinon None.
    """
    if not classified_key:
        return None
    # Direction 1 : LLM a tronqué → expected name starts with classified key
    candidates_a = [
        k for k in expected_keys
        if k.startswith(classified_key + " ") or k == classified_key
    ]
    # Direction 2 : LLM a paraphrasé en allongeant → classified key starts with expected
    candidates_b = [
        k for k in expected_keys
        if classified_key.startswith(k + " ") or classified_key == k
    ]
    candidates = list({*candidates_a, *candidates_b})
    return candidates[0] if len(candidates) == 1 else None


def match_classified_to_expected(
    classified: list[dict[str, Any]],
    expected_for_jalons: list[dict[str, Any]],
    project_type: str,
) -> tuple[list[ExpectedDocument], list[dict[str, Any]]]:
    """Renvoie (documents_par_jalon, fichiers_orphelins).

    - `classified` : liste de dicts {file: FileMetadata, type, confidence, reason, file_hash, status_extraction}
    - `expected_for_jalons` : liste d'entrées du référentiel V11 (jalons.documents aplatis)
    - `project_type` : 'AgriPV' | 'S21' — pour gérer les conditionnels
    """
    # Index des classifiés par type normalisé → tous les candidats
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    matched_ids: set[str] = set()

    # 2-passes : d'abord exact match, puis prefix-match pour les orphelins.
    expected_keys = [_normalize_type(e["name"]) for e in expected_for_jalons]
    expected_keys_set = list(set(expected_keys))

    for c in classified:
        ctype = c.get("classified_type")
        if not ctype:
            continue
        key = _normalize_type(ctype)
        if key in expected_keys_set:
            by_type[key].append(c)
        else:
            # Fallback : prefix-match si UN seul expected matche
            alias = _find_prefix_match(key, expected_keys_set)
            if alias is not None:
                by_type[alias].append(c)
            else:
                by_type[key].append(c)  # restera orphelin si pas dans expected

    result: list[ExpectedDocument] = []

    for exp in expected_for_jalons:
        key = _normalize_type(exp["name"])
        candidates = by_type.get(key, [])

        # Trier par confidence descendante
        candidates_sorted = sorted(candidates, key=lambda c: -(c.get("confidence") or 0))

        # Cas particulier : Attestation MSA → uniquement si AgriPV
        propriete = exp.get("propriete", "Obligatoire")
        if "msa" in _normalize_type(exp["name"]) and project_type != "AgriPV":
            result.append(
                ExpectedDocument(
                    code=exp["code"],
                    name=exp["name"],
                    propriete=propriete,
                    status="not_applicable",
                    found_files=[],
                    note=exp.get("note"),
                )
            )
            continue

        if not candidates_sorted:
            # « Cas par cas » : conditionnellement applicable. Sans candidat,
            # on ne marque PAS comme défaut — l'UI montrera la note métier.
            status = "not_applicable" if propriete == "Cas par cas" else "missing"
            result.append(
                ExpectedDocument(
                    code=exp["code"],
                    name=exp["name"],
                    propriete=propriete,
                    status=status,
                    found_files=[],
                    note=exp.get("note"),
                )
            )
            continue

        best_conf = candidates_sorted[0]["confidence"] or 0
        status_tier = tier(best_conf)
        status = status_tier  # present | ambiguous | missing

        found = []
        for c in candidates_sorted:
            file: FileMetadata = c["file"]
            found.append(
                FoundFile(
                    file_name=file.name,
                    sharepoint_url=file.url,
                    sharepoint_path=file.path,
                    confidence=c.get("confidence") or 0,
                    reason=c.get("reason") or "",
                    file_hash=c.get("file_hash"),
                )
            )
            matched_ids.add(file.path)

        result.append(
            ExpectedDocument(
                code=exp["code"],
                name=exp["name"],
                propriete=propriete,
                status=status,
                found_files=found,
                note=exp.get("note"),
            )
        )

    # Fichiers orphelins : classifiés non rattachés à un attendu
    orphans = [c for c in classified if c.get("file") and c["file"].path not in matched_ids]
    return result, orphans
