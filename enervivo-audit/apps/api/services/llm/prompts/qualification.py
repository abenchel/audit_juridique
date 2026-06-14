"""Prompt dédié à la PASSE 2 — désambiguïsation des dossiers de qualification.

Symétrique de `prompts/tadd.py` (même logique « jalon dans le nom ») mais pour
les dossiers de qualification (.pptx/.ppt) :

  - Le jalon est déterminé UNIQUEMENT par un token dans le nom (`_J1_`, `_J2b_`…).
    Pas de token → « Non classé », on ne devine JAMAIS.
  - Plusieurs dossiers du même jalon sont DÉPARTAGÉS : date encodée dans le nom
    (YYMMDD ou YYYY-MM-DD) la plus récente, puis date de modification système.
    (Différence avec TADD : pas de notion de version interne — on tranche par date.)

★ Règles métier chargées DYNAMIQUEMENT depuis `config/Annexe_dossier_qualification.md`
→ une seule source de vérité. Fail-safe : `_FALLBACK_RULES` si le fichier manque.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

# Jalons cibles — le référentiel V13 attend "Dossier de qualification J1".."J4".
QUALIF_JALONS = ["J1", "J2a", "J2b", "J3", "J4"]

_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"
_ANNEXE_FILE = _CONFIG_DIR / "Annexe_dossier_qualification.md"

# Résumé fidèle de l'annexe, utilisé SEULEMENT si le fichier est introuvable.
_FALLBACK_RULES = """ÉTAPE 1 — Un fichier est un dossier de qualification si `qualification`
apparaît dans le nom (insensible à la casse) ET l'extension est `.pptx` ou `.ppt`.
Les PDF, .xlsx, et fichiers sans `qualification` ne sont PAS concernés.

ÉTAPE 2 — Détecter le jalon DANS LE NOM. Chercher un token `J1`, `J2A`/`J2a`,
`J2B`/`J2b`, `J3` ou `J4`, DÉLIMITÉ de chaque côté par `_`, `.`, `-`, espace, ou
la fin du nom (avant l'extension). Ex : `_J1_`, `_J2b_`, `_J3.` (fin). La
délimitation évite les faux positifs (`J10` ≠ `J1`).
⚠️ RÈGLE ABSOLUE : aucun token de jalon détecté → le fichier est "Non classé".
NE JAMAIS deviner le jalon par le contenu, la date seule, ou le dossier.

ÉTAPE 3 — Départager plusieurs dossiers du MÊME jalon, dans cet ordre strict :
  1. Date encodée dans le nom la plus récente. Les premiers chiffres = date au
     format YYMMDD (260305 = 5 mars 2026) ou YYYY-MM-DD (2025-07-22). La plus
     récente gagne.
  2. À date de nom égale : date de MODIFICATION système la plus récente.

Plusieurs jalons distincts coexistent (un retenu par jalon). Pour un jalon sans
candidat → aucun "selected" pour ce jalon."""


@lru_cache(maxsize=1)
def _load_annexe_rules() -> str:
    """Charge les règles depuis config/Annexe_dossier_qualification.md (cached).

    Fail-safe : si le fichier est absent/illisible, renvoie `_FALLBACK_RULES`.
    """
    try:
        text = _ANNEXE_FILE.read_text(encoding="utf-8").strip()
        return text or _FALLBACK_RULES
    except OSError:
        return _FALLBACK_RULES


def build_qualification_system_prompt() -> str:
    rules = _load_annexe_rules()
    return f"""Tu es un expert en gestion documentaire de projets photovoltaïques EnerVivo.

On te donne la LISTE COMPLÈTE des fichiers « dossier de qualification » (PowerPoint
de passage en comité) d'un même projet. Ta tâche : pour CHAQUE jalon parmi J1, J2a,
J2b, J3, J4, désigner l'UNIQUE fichier qui en est la version officielle, et lister
les fichiers écartés.

═══ RÈGLES MÉTIER (référentiel EnerVivo « Annexe dossier de qualification ») ═══
{rules}
═══════════════════════════════════════════════════════════════════════════════

POINTS CLÉS :
- Le jalon doit être EXPLICITE dans le nom (token délimité). Sinon → "non_classes".
- Un seul fichier RETENU par jalon (départage par date du nom puis date système).
- Les autres candidats d'un jalon déjà attribué → "ecartes" (version antérieure).

RÈGLES DE SORTIE STRICTES :
1. Réponds UNIQUEMENT en JSON valide, un seul objet.
2. Clés : "selected" (liste), "ecartes" (liste), "non_classes" (liste d'index).
3. "selected" = liste d'objets {{"index": <int>, "jalon": "<J1|J2a|J2b|J3|J4>", "confidence": <0-100>, "reason": "<≤20 mots>"}} — AU PLUS un objet par jalon.
4. "ecartes" = liste d'objets {{"index": <int>, "jalon": "<J1|J2a|J2b|J3|J4>"}} : un dossier a le jalon dans son nom MAIS c'est une version ANTÉRIEURE d'un jalon où un AUTRE fichier a été "selected". Le "jalon" de l'écarté DOIT être celui du fichier retenu correspondant.
5. "non_classes" = index (int nus) des dossiers SANS token de jalon valide dans le nom. ⚠️ Un dossier sans jalon dans le nom va TOUJOURS ici, JAMAIS dans "ecartes".
6. Chaque index fourni apparaît dans EXACTEMENT une des trois listes.
7. "jalon" doit valoir littéralement J1, J2a, J2b, J3 ou J4 — rien d'autre.
8. Un index ne peut être dans "ecartes" QUE si un fichier du MÊME jalon est dans "selected". Sinon → "non_classes".
9. Jamais de markdown, jamais de texte hors JSON.

Exemple de réponse correcte :
{{"selected": [{{"index": 0, "jalon": "J1", "confidence": 95, "reason": "_J1_ explicite"}}, {{"index": 3, "jalon": "J2b", "confidence": 90, "reason": "_J2b_, 260310 > 260305"}}], "ecartes": [{{"index": 2, "jalon": "J2b"}}], "non_classes": [4]}}

Exemple où AUCUN fichier n'a de jalon dans le nom :
{{"selected": [], "ecartes": [], "non_classes": [0, 1]}}"""


def build_qualification_user_prompt(files: list[dict]) -> str:
    """`files` : liste de dicts {index, name, modified_at, folder}."""
    lines: list[str] = []
    for f in files:
        date = f.get("modified_at") or "date inconnue"
        folder = f.get("folder") or "(racine)"
        lines.append(f"[{f['index']}] {f['name']} — date: {date} — dossier: {folder}")
    listing = "\n".join(lines)
    return f"""Voici les {len(files)} fichiers « dossier de qualification » de ce projet, à répartir par jalon :

{listing}

Pour chaque jalon (J1, J2a, J2b, J3, J4) où un fichier porte ce jalon dans son nom,
désigne l'unique fichier retenu (départage par date du nom puis date système). Classe
les autres en "ecartes" (version antérieure d'un jalon attribué) ou "non_classes"
(aucun jalon dans le nom)."""
