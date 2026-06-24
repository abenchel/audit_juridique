"""Versioning métier de l'outil — lecture de config/tool_version.json.

La version de l'outil est gérée À LA MAIN dans config/tool_version.json (comme un
changelog / des commits) : l'utilisateur ajoute une entrée {version, date,
description} à chaque changement métier (référentiel, annexe, prompt…). La version
COURANTE = la dernière entrée du tableau.

Usages :
  - chaque audit enregistre `current_version()` à son lancement (audits.tool_version) ;
  - chaque classification enregistre la version qui l'a produite
    (classified_documents.tool_version) ; au cache-hit on hérite la version
    d'origine, donc la « version du cache » d'un audit = `oldest_version(...)`
    de ses classifications ;
  - le changelog admin renvoie `full_changelog()`.

Fail-safe TOTAL : si le fichier est absent/illisible/invalide, on renvoie une
liste vide / None et on log un warning — JAMAIS d'exception (un audit ne doit
pas planter pour un souci de versioning).

Le fichier est rechargé si son mtime change (les process API/worker sont longs ;
un simple lru_cache figerait la version jusqu'au restart).
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

# services/version.py → parents[1] = apps/api/ → config/
_VERSION_FILE = Path(__file__).resolve().parents[1] / "config" / "tool_version.json"

# Cache simple invalidé par mtime (pas de lru_cache qui figerait jusqu'au restart).
_cache: dict[str, Any] = {"mtime": None, "data": []}


def _version_sort_key(version: str | None) -> tuple[int, int]:
    """Clé de tri NUMÉRIQUE pour 'V1', 'V2', …, 'V10'.

    Garde-fou contre le tri lexical où 'V10' < 'V2'. Les valeurs non
    reconnues (None, format inattendu) sont triées en fin (rang max).
    """
    if not version:
        return (1, 0)
    m = re.match(r"^[Vv](\d+)$", version.strip())
    if not m:
        return (1, 0)
    return (0, int(m.group(1)))


def full_changelog() -> list[dict[str, Any]]:
    """Liste complète des versions [{version, date, description}], ordre du fichier.

    Fail-safe : [] si fichier absent/illisible/invalide.
    """
    try:
        st = _VERSION_FILE.stat()
    except OSError:
        return []

    if _cache["mtime"] != st.st_mtime:
        try:
            raw = json.loads(_VERSION_FILE.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValueError("tool_version.json doit être un tableau JSON")
            _cache["data"] = raw
            _cache["mtime"] = st.st_mtime
        except (OSError, ValueError, json.JSONDecodeError) as e:
            log.warning("tool_version.json illisible (%s) — changelog vide", e)
            return []
    return list(_cache["data"])


def current_version() -> str | None:
    """Version courante = dernière entrée du changelog (ou None si vide)."""
    entries = full_changelog()
    if not entries:
        return None
    last = entries[-1]
    v = last.get("version") if isinstance(last, dict) else None
    return str(v) if v else None


def oldest_version(versions: list[str | None]) -> str | None:
    """Plus ancienne version (ordre numérique) parmi une liste, en ignorant les None.

    Sert à calculer la « version du cache » d'un audit = min des tool_version
    de ses classifications. Renvoie None si la liste ne contient que des None/vide.
    """
    valid = [v for v in versions if v]
    if not valid:
        return None
    return min(valid, key=_version_sort_key)
