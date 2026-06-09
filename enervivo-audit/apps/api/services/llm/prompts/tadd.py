"""Prompt dédié à la PASSE 2 — désambiguïsation des TADD par jalon.

Symétrique de `prompts/plan_masse.py`, mais la logique métier diffère :

  - PLAN DE MASSE : le jalon n'est JAMAIS dans le nom → déduit par dates/patterns,
    et CHAQUE plan reçoit un jalon (pas de départage).
  - TADD : le jalon est SOUVENT explicite dans le nom (`_J1_`, `_J2B_`…). Règle
    stricte : pas de token de jalon dans le nom → "Non classé", on ne devine
    JAMAIS. Et plusieurs TADD du même jalon doivent être DÉPARTAGÉS (un seul
    retenu : version interne la plus haute, puis date) — les perdants ne comptent
    pas comme la version officielle du jalon.

★ Les règles métier (détection du token jalon, normalisation des versions, ordre
de départage) sont chargées DYNAMIQUEMENT depuis `config/Annexe_fichier_TADD.md`
→ une seule source de vérité : modifier l'annexe = le prompt suit (après rebuild
de l'image, le .md y est baké). Fail-safe : si le fichier est introuvable, on
retombe sur les règles en dur `_FALLBACK_RULES` ci-dessous (jamais de casse).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

# Jalons cibles dans l'ordre chronologique du référentiel V13 (identiques au
# plan de masse : le référentiel attend "TADD version J1".."TADD version J4").
TADD_JALONS = ["J1", "J2a", "J2b", "J3", "J4"]

# Même convention de chemin que prompts/juridique.py : remonter à apps/api/config.
_CONFIG_DIR = Path(__file__).resolve().parents[3] / "config"
_ANNEXE_FILE = _CONFIG_DIR / "Annexe_fichier_TADD.md"

# Règles en dur — utilisées SEULEMENT si l'annexe est introuvable (fail-safe).
# Doivent rester un résumé fidèle de Annexe_fichier_TADD.md.
_FALLBACK_RULES = """ÉTAPE 1 — Un fichier est un TADD si `TADD` apparaît dans le nom (insensible
à la casse) ET l'extension est `.xlsm` ou `.xlsb`. Les `.xlsx` simples, PDF et
fichiers sans `TADD` ne sont pas des TADD.

ÉTAPE 2 — Détecter le jalon DANS LE NOM. Chercher un token `J1`, `J2A`/`J2a`,
`J2B`/`J2b`, `J3` ou `J4`, DÉLIMITÉ de chaque côté par `_`, `.`, `-`, espace, ou
la fin du nom (avant l'extension). Ex : `_J1_`, `-J4-`, `_J3.` (fin). Cette
délimitation évite les faux positifs (`J10` ≠ `J1`).
⚠️ RÈGLE ABSOLUE : aucun token de jalon détecté → le fichier est "Non classé".
NE JAMAIS deviner le jalon par d'autres indices (dates, dossier, contenu).

ÉTAPE 3 — Départager plusieurs TADD du MÊME jalon, dans cet ordre strict :
  1. Version interne la plus haute. Le `vX[._]Y[._]Z` du nom = version du modèle
     TADD VivEpic (PAS le jalon). Normaliser `_`→`.` puis comparer comme un tuple
     d'entiers : v6.6.10 (6,6,10) > v6.6 (6,6) > v6 (6,) > v5 (5,).
  2. À version égale : date de MODIFICATION système la plus récente.
  3. À date égale : `YYMMDD` en tête de nom le plus récent.

Plusieurs jalons distincts peuvent coexister (un retenu par jalon). Pour chaque
jalon sans aucun candidat → simplement aucun "selected" pour ce jalon."""


@lru_cache(maxsize=1)
def _load_annexe_rules() -> str:
    """Charge les règles depuis config/Annexe_fichier_TADD.md (cached).

    Fail-safe : si le fichier est absent/illisible, renvoie `_FALLBACK_RULES`.
    """
    try:
        text = _ANNEXE_FILE.read_text(encoding="utf-8").strip()
        return text or _FALLBACK_RULES
    except OSError:
        return _FALLBACK_RULES


def build_tadd_system_prompt() -> str:
    rules = _load_annexe_rules()
    return f"""Tu es un expert en gestion documentaire de projets photovoltaïques EnerVivo.

On te donne la LISTE COMPLÈTE des fichiers « TADD » (Tableau d'Aide À la Décision)
d'un même projet. Ta tâche : pour CHAQUE jalon parmi J1, J2a, J2b, J3, J4, désigner
l'UNIQUE fichier TADD qui en est la version officielle, et lister les fichiers
écartés.

═══ RÈGLES MÉTIER (référentiel EnerVivo « Annexe fichier TADD ») ═══
{rules}
═══════════════════════════════════════════════════════════════════

POINTS CLÉS :
- Le jalon doit être EXPLICITE dans le nom (token délimité). Sinon → "non_classes".
- Un seul fichier RETENU par jalon (départage par version interne puis date).
- Les autres candidats d'un jalon déjà attribué → "ecartes" (version antérieure).

RÈGLES DE SORTIE STRICTES :
1. Réponds UNIQUEMENT en JSON valide, un seul objet.
2. Clés : "selected" (liste), "ecartes" (liste), "non_classes" (liste d'index).
3. "selected" = liste d'objets {{"index": <int>, "jalon": "<J1|J2a|J2b|J3|J4>", "confidence": <0-100>, "reason": "<≤20 mots>"}} — AU PLUS un objet par jalon.
4. "ecartes" = liste d'objets {{"index": <int>, "jalon": "<J1|J2a|J2b|J3|J4>"}} : un TADD a le jalon dans son nom MAIS c'est une version ANTÉRIEURE d'un jalon où un AUTRE fichier a été "selected". Le "jalon" de l'écarté DOIT être le même que celui du fichier retenu correspondant.
5. "non_classes" = index (int nus) des TADD SANS token de jalon valide dans le nom. ⚠️ Un TADD sans jalon dans le nom va TOUJOURS ici, JAMAIS dans "ecartes".
6. Chaque index fourni apparaît dans EXACTEMENT une des trois listes.
7. "jalon" doit valoir littéralement J1, J2a, J2b, J3 ou J4 — rien d'autre.
8. Un index ne peut être dans "ecartes" QUE si un fichier du MÊME jalon est dans "selected". Sinon → "non_classes".
9. Jamais de markdown, jamais de texte hors JSON.

Exemple de réponse correcte :
{{"selected": [{{"index": 0, "jalon": "J1", "confidence": 95, "reason": "_J1_ explicite, v6.6.10 la plus haute"}}, {{"index": 2, "jalon": "J3", "confidence": 90, "reason": "_J3 explicite"}}], "ecartes": [{{"index": 1, "jalon": "J1"}}], "non_classes": [3]}}

Exemple où AUCUN fichier n'a de jalon dans le nom (cas fréquent) :
{{"selected": [], "ecartes": [], "non_classes": [0, 1, 2]}}"""


def build_tadd_user_prompt(files: list[dict]) -> str:
    """`files` : liste de dicts {index, name, modified_at, folder}."""
    lines: list[str] = []
    for f in files:
        date = f.get("modified_at") or "date inconnue"
        folder = f.get("folder") or "(racine)"
        lines.append(f"[{f['index']}] {f['name']} — date: {date} — dossier: {folder}")
    listing = "\n".join(lines)
    return f"""Voici les {len(files)} fichiers « TADD » de ce projet, à répartir par jalon :

{listing}

Pour chaque jalon (J1, J2a, J2b, J3, J4) où un fichier porte ce jalon dans son nom,
désigne l'unique fichier retenu (départage par version puis date). Classe les autres
en "ecartes" (version antérieure d'un jalon attribué) ou "non_classes" (aucun jalon
dans le nom)."""
