"""Audit juridique — charge V11 (par jalon) et l'enrichit avec V2 (par dossier).

V11 reste la source de vérité pour « quel doc est attendu à quel jalon ».
V2 apporte des indices contextuels (folder_path, extensions, comment) que
le prompt LLM utilisera pour mieux disambiguer (ex. un "Devis" trouvé dans
/10-Raccordement n'est pas un EPA même si tous les deux sont des devis).

Jointure : token-set fuzzy match (stdlib difflib) sur les noms normalisés.
Seuil 0.55 — un peu permissif car V2 ajoute souvent des qualificatifs
("Bail signe (toutes versions)" vs V11 "Bail signe"). Faux positifs gérés
par la confidence LLM lors de la classification.
"""

from __future__ import annotations

import json
import logging
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from .base import AuditTypeHandler

log = logging.getLogger(__name__)

_CONFIG = Path(__file__).resolve().parents[3] / "config"
V11_PATH = _CONFIG / "documents_v12.json"  # nom de variable historique, contenu V12
V2_PATH = _CONFIG / "documents_projet_v2.json"

# Seuil minimal pour rapprocher V11 ↔ V2 sur les noms.
# 0.45 = ~60% des mots V11 retrouvés dans V2 (+ un peu de jaccard).
_FUZZY_THRESHOLD = 0.45
# Seuil pour la passe 2 (fallback folder-based) : au moins 1 token V11 apparaît
# dans le folder_path ou le name de V2 entries du même dossier.
_FOLDER_MIN_HITS = 1

# Mots vides qu'on ignore lors de la comparaison (sinon "de", "la", "le"
# faussent le score).
_STOP_WORDS = frozenset({
    "de", "du", "des", "la", "le", "les", "l", "un", "une", "et", "ou",
    "a", "au", "aux", "en", "par", "pour", "sur", "dans", "avec",
    "ou", "si", "version", "projet", "documents", "document",
})


def _tokens(s: str) -> set[str]:
    """Lowercase + strip accents + tokenize (mots de >=2 chars sans stop-words)."""
    nfkd = unicodedata.normalize("NFKD", s)
    ascii_s = nfkd.encode("ascii", "ignore").decode("ascii").lower()
    words = re.findall(r"[a-z0-9]{2,}", ascii_s)
    return {w for w in words if w not in _STOP_WORDS}


def _similarity(a: str, b: str) -> float:
    """Score 0..1 combinant containment de A dans B + Jaccard global.

    Robuste aux différences de longueur (V11 noms courts, V2 noms enrichis).
    Ex : "LOI signee" vs "LOI signee (Lettre d'Intention)" → score ≈ 0.82.
    """
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    inter = ta & tb
    if not inter:
        return 0.0
    containment = len(inter) / len(ta)  # % de mots V11 trouvés dans V2
    jaccard = len(inter) / len(ta | tb)
    return 0.7 * containment + 0.3 * jaccard


def _find_folder_by_tokens(v11_name: str, v2_docs: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Passe 2 (fallback) : aucune correspondance fine trouvée. On regarde si
    un mot distinctif de V11 apparaît dans le folder_path d'un dossier V2 → on
    propose ce dossier comme hint (sans matcher un nom précis).

    Ex : V11 "Devis signé EPA" → token "epa" apparaît dans le folder
    "7-Achat-Fournisseurs/1-Consultations/EPA" → hint folder.
    """
    v11_tokens = _tokens(v11_name)
    # Ignore les tokens trop génériques en fallback (peu discriminants)
    distinctive = {t for t in v11_tokens if len(t) >= 3}
    if not distinctive:
        return None

    # Compte les hits par folder_path
    hits_by_folder: dict[str, int] = {}
    examples_by_folder: dict[str, list[str]] = {}
    for v2_doc in v2_docs:
        folder = v2_doc["folder_path"]
        folder_tokens = _tokens(folder)
        common = distinctive & folder_tokens
        if common:
            # Score = nombre de tokens V11 distinctifs présents dans le folder
            hits_by_folder[folder] = max(hits_by_folder.get(folder, 0), len(common))
            examples_by_folder.setdefault(folder, []).append(v2_doc["name"])

    if not hits_by_folder:
        return None

    # Prend le folder avec le plus de hits, en cas d'égalité le plus profond
    best_folder = max(
        hits_by_folder.items(),
        key=lambda x: (x[1], x[0].count("/")),
    )[0]
    hits = hits_by_folder[best_folder]
    if hits < _FOLDER_MIN_HITS:
        return None

    # Récupère les extensions en agrégeant celles des V2 docs du même folder
    extensions: list[str] = []
    for v2_doc in v2_docs:
        if v2_doc["folder_path"] == best_folder:
            for e in v2_doc.get("extensions", []):
                if e not in extensions:
                    extensions.append(e)

    return {
        "score": None,  # match folder uniquement, pas de score nom
        "name": None,
        "folder_path": best_folder,
        "extensions": extensions,
        "comment": "Match par dossier (pas par nom direct)",
        "examples": examples_by_folder[best_folder][:3],
    }


def _enrich_v11_with_v2(v11: dict[str, Any], v2: dict[str, Any]) -> dict[str, Any]:
    """Pour chaque doc V11, attache le meilleur match V2 (s'il dépasse le seuil).

    2 passes :
      - Passe 1 (nom fin) : best fuzzy match sur le nom V2 (seuil _FUZZY_THRESHOLD).
      - Passe 2 (folder fallback) : si la passe 1 a échoué, on regarde si un
        token V11 distinctif apparaît dans un folder V2 — on prend ce folder
        comme hint (sans matcher un nom précis).

    L'enrichissement est non-destructif : V11 garde ses champs originaux,
    on ajoute juste `v2_match` avec folder_path + extensions + comment.
    """
    v2_docs: list[dict[str, Any]] = v2.get("documents", [])
    if not v2_docs:
        return v11

    matched_name = 0
    matched_folder = 0
    total = 0
    for jalon in v11.get("jalons", []):
        for doc in jalon.get("documents", []):
            total += 1
            name = doc["name"]
            # Passe 1 : fuzzy sur le nom
            best: tuple[float, dict[str, Any] | None] = (0.0, None)
            for v2_doc in v2_docs:
                score = _similarity(name, v2_doc["name"])
                if score > best[0]:
                    best = (score, v2_doc)

            if best[1] is not None and best[0] >= _FUZZY_THRESHOLD:
                v2_doc = best[1]
                doc["v2_match"] = {
                    "score": round(best[0], 2),
                    "name": v2_doc["name"],
                    "folder_path": v2_doc.get("folder_path"),
                    "extensions": v2_doc.get("extensions") or [],
                    "comment": v2_doc.get("comment") or "",
                    "via": "name",
                }
                matched_name += 1
                continue

            # Passe 2 : folder fallback
            folder_match = _find_folder_by_tokens(name, v2_docs)
            if folder_match is not None:
                folder_match["via"] = "folder"
                doc["v2_match"] = folder_match
                matched_folder += 1

    log.info(
        "Enrichissement V11 x V2 : %d/%d matchés par nom + %d par folder (seuil nom %.2f)",
        matched_name, total, matched_folder, _FUZZY_THRESHOLD,
    )
    v11["_enriched_with"] = v2.get("version", "V2")
    v11["_match_stats"] = {
        "matched_name": matched_name,
        "matched_folder": matched_folder,
        "total": total,
    }
    return v11


@lru_cache(maxsize=1)
def _load_reference() -> dict[str, Any]:
    if not V11_PATH.exists():
        raise FileNotFoundError(
            f"Référentiel introuvable à {V11_PATH}. "
            "Lance : python -m scripts.convert_excel_to_json --in ../260518_Document_par_Jalon_V13.xlsx --version V13"
        )
    v11 = json.loads(V11_PATH.read_text(encoding="utf-8"))

    if V2_PATH.exists():
        v2 = json.loads(V2_PATH.read_text(encoding="utf-8"))
        v11 = _enrich_v11_with_v2(v11, v2)
    else:
        log.warning(
            "V2 absent (%s) — pas d'enrichissement folder/extensions. "
            "Lance scripts/convert_liste_projet_to_json.py pour le générer.",
            V2_PATH,
        )
    return v11


class JuridiqueAudit(AuditTypeHandler):
    @property
    def audit_type(self) -> str:
        return "juridique"

    def load_reference(self) -> dict[str, Any]:
        return _load_reference()
