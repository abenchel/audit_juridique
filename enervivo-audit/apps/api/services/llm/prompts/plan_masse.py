"""Prompt dédié à la PASSE 2 — désambiguïsation des plans de masse par jalon.

Problème résolu : en passe 1 le LLM voit chaque fichier ISOLÉMENT. Un plan de
masse ne porte JAMAIS son jalon dans le nom (pas de `_J1_`), donc le LLM ne peut
pas savoir si c'est la version J1, J2a, J2b, J3 ou J4 — il les confond.

En passe 2 on rassemble TOUS les plans de masse d'un projet et on les soumet en
UN SEUL appel : le LLM a alors le contexte global (liste complète + dates +
dossiers) et peut appliquer les patterns de nommage + l'ordre chronologique.

★ Les règles métier (patterns _APS_/_APD_/_PC_/_EXE_, indices de révision, tri
chronologique) sont chargées DYNAMIQUEMENT depuis `config/annexe_plan_masse.md`
→ une seule source de vérité : modifier l'annexe = le prompt suit (après rebuild
de l'image, le .md y est baké). Fail-safe : si le fichier est introuvable, on
retombe sur les règles en dur `_FALLBACK_RULES` ci-dessous (jamais de casse).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

# Jalons cibles dans l'ordre chronologique du référentiel V12.
PLAN_MASSE_JALONS = ["J1", "J2a", "J2b", "J3", "J4"]

# Même convention de chemin que prompts/juridique.py : remonter à apps/api/config.
_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"
_ANNEXE_FILE = _CONFIG_DIR / "annexe_plan_masse.md"

# Règles en dur — utilisées SEULEMENT si l'annexe est introuvable (fail-safe).
# Doivent rester un résumé fidèle de annexe_plan_masse.md.
_FALLBACK_RULES = """PATTERNS DE NOMMAGE (indice principal) :
- `_APS_`                         → J1   (Avant-Projet Sommaire = version la plus précoce)
- `_APD_`                         → J2a  (Avant-Projet Détaillé = affinage post-J1)
- `_depot_PC_` / `_PC0_` / `_DP_` → J2b  (version jointe au dépôt du Permis de Construire / Déclaration Préalable)
- `_EXE_` / `_PRO_`               → J3 ou J4 (Exécution / Projet = versions finales pré-construction)

⚠️ Les indices de RÉVISION (`Ind A`, `Ind B`, `Ind C`...) ne correspondent PAS
aux jalons. Ce sont de simples marqueurs chronologiques de révisions d'un même
plan, indépendants du jalon. Un `Ind A` peut exister à n'importe quel jalon.

STRATÉGIE SI LE NOM EST AMBIGU (pas de pattern ci-dessus) :
1. Trie par DATE (champ fourni, ou préfixe `YYMMDD_` du nom) : le plus ancien = J1,
   les suivants J2a, J2b, J3, J4 par ordre chronologique croissant.
2. Un dossier `old/` ou `0 - OLD/` indique souvent une version archivée précoce (J1/J2a).
3. Compare les indices de révision `Ind A < Ind B < Ind C` comme ordre chronologique
   secondaire (sans lien direct avec le jalon).
4. Plusieurs plans peuvent légitimement tomber sur le MÊME jalon — ne force pas 1:1."""


@lru_cache(maxsize=1)
def _load_annexe_rules() -> str:
    """Charge les règles depuis config/annexe_plan_masse.md (cached).

    Fail-safe : si le fichier est absent/illisible, renvoie `_FALLBACK_RULES`.
    """
    try:
        text = _ANNEXE_FILE.read_text(encoding="utf-8").strip()
        return text or _FALLBACK_RULES
    except OSError:
        return _FALLBACK_RULES


def build_plan_masse_system_prompt() -> str:
    rules = _load_annexe_rules()
    return f"""Tu es un expert en gestion documentaire de projets photovoltaïques EnerVivo.

On te donne la LISTE COMPLÈTE des fichiers « Plan de masse » d'un même projet.
Ta tâche : attribuer à CHACUN le jalon auquel il appartient, parmi exactement :
J1, J2a, J2b, J3, J4.

⚠️ Le jalon n'est JAMAIS écrit explicitement dans le nom (pas de `_J1_`, `_J2a_`).
Tu dois le DÉDUIRE à partir d'indices secondaires, selon les règles métier suivantes :

═══ RÈGLES MÉTIER (référentiel EnerVivo « Annexe plan de masse ») ═══
{rules}
═══════════════════════════════════════════════════════════════════

Si vraiment indéterminable après ces règles, choisis le jalon le plus plausible
par la date et indique une confidence basse.

RÈGLES DE SORTIE STRICTES :
1. Réponds UNIQUEMENT en JSON valide, un seul objet avec la clé "assignments".
2. "assignments" = liste d'objets {{"index": <int>, "jalon": "<J1|J2a|J2b|J3|J4>", "confidence": <0-100>, "reason": "<≤20 mots>"}}.
3. Il doit y avoir EXACTEMENT un objet par fichier fourni (même index).
4. "jalon" doit valoir littéralement J1, J2a, J2b, J3 ou J4 — rien d'autre.
5. Jamais de markdown, jamais de texte hors JSON.

Exemple de réponse correcte :
{{"assignments": [{{"index": 0, "jalon": "J1", "confidence": 90, "reason": "_APS_ explicite, plan le plus ancien"}}, {{"index": 1, "jalon": "J2b", "confidence": 85, "reason": "_depot_PC_ explicite"}}]}}"""


def build_plan_masse_user_prompt(files: list[dict]) -> str:
    """`files` : liste de dicts {index, name, modified_at, folder}."""
    lines: list[str] = []
    for f in files:
        date = f.get("modified_at") or "date inconnue"
        folder = f.get("folder") or "(racine)"
        lines.append(f"[{f['index']}] {f['name']} — date: {date} — dossier: {folder}")
    listing = "\n".join(lines)
    return f"""Voici les {len(files)} fichiers « Plan de masse » de ce projet, à répartir par jalon :

{listing}

Attribue un jalon (J1, J2a, J2b, J3 ou J4) à CHAQUE fichier ci-dessus."""
