"""Prompt système d'audit juridique — généré dynamiquement depuis documents_v12.json.

Aligne le LLM sur la liste exacte des types de documents attendus, pour réduire
les hallucinations et faciliter le matching. Si le référentiel a été enrichi
avec V2 (`v2_match` présent sur les docs), on inclut aussi pour chaque type :
le dossier où il est censé se trouver et les extensions attendues.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

_DESCRIPTIONS_FILE = (
    Path(__file__).resolve().parents[3] / "config" / "descriptions_part1.md"
)


@lru_cache(maxsize=1)
def _load_enriched_descriptions() -> str:
    """Charge le référentiel V12 enrichi (descriptions_part1.md) si présent.

    Document métier détaillé par type : définition, format observé, indices internes,
    nommage, stratégie de classification, pièges. Servi en knowledge base au LLM,
    mis en cache OpenRouter (ephemeral) pour ne coûter qu'une fois par batch.
    """
    try:
        return _DESCRIPTIONS_FILE.read_text(encoding="utf-8")
    except OSError:
        return ""


def _format_hint(v2: dict[str, Any] | None) -> str:
    """Construit le hint folder + extensions à partir du v2_match (peut être None).

    Renvoie chaîne vide si aucun hint utile.
    """
    if not v2:
        return ""
    folder = v2.get("folder_path") or ""
    extensions = v2.get("extensions") or []
    comment = v2.get("comment") or ""

    parts: list[str] = []
    if folder:
        parts.append(f"dossier : {folder}")
    if extensions:
        parts.append(f"ext : {', '.join(extensions)}")
    if comment and "Match par dossier" not in comment:
        # On ne ré-affiche pas la note technique du match folder
        parts.append(f"note : {comment}")
    return f"  ({' ; '.join(parts)})" if parts else ""


def build_system_prompt(documents_v11: dict[str, Any]) -> str:
    """Construit le prompt système à partir du référentiel V11 (enrichi V2 si dispo)."""
    types_lines: list[str] = []
    seen: set[str] = set()
    for jalon in documents_v11.get("jalons", []):
        for doc in jalon.get("documents", []):
            name = doc["name"].strip()
            if name in seen:
                continue
            seen.add(name)
            hint = _format_hint(doc.get("v2_match"))
            types_lines.append(f"- {name}{hint}")

    types_list = "\n".join(types_lines)
    has_hints = documents_v11.get("_enriched_with") is not None

    hint_paragraph = ""
    if has_hints:
        hint_paragraph = """

Pour chaque type ci-dessus tu as parfois entre parenthèses des indices issus
du template projet EnerVivo de référence (V2). ⚠️ **TOUS ces indices sont
PUREMENT INDICATIFS — jamais des filtres stricts.** Les vrais projets
s'organisent librement (arborescences différentes, noms FR/EN, conventions
de nommage variables, extensions inhabituelles, etc.). Ne rejette JAMAIS une
classification cohérente avec le contenu juste parce qu'un indice ne colle pas.

  - "dossier" = l'emplacement DE RÉFÉRENCE dans l'arborescence type EnerVivo
    (ex. "4-Documents Administratifs/6-Bail/PDB"). Sert à départager deux
    types proches (ex. "Devis EPA" vs "Devis Enviro" ont des dossiers de
    référence distincts) — si tu vois des mots-clés du dossier dans le path
    réel, c'est un bonus de confidence ; sinon ce n'est PAS un malus.
  - "ext" = les extensions typiquement associées (.pdf, .docx, .pptx…).
    Indicatif : un projet peut avoir scanné une LOI en .jpg, ou exporté un
    bail en .docx au lieu de .pdf. Ne rejette pas pour un mismatch d'ext.
  - "note" = condition d'applicabilité ou contexte (ex. "Si projet AgriPV",
    "Si proprietaire = personne morale"). Aide à comprendre le type, n'impose
    rien."""

    enriched = _load_enriched_descriptions()
    descriptions_block = ""
    if enriched:
        descriptions_block = f"""

---

📚 RÉFÉRENTIEL ENRICHI V12 — descriptions métier détaillées par type de document.
Pour CHAQUE type ci-dessus tu disposes ci-dessous d'une fiche : définition, format
observé, indices internes typiques (en-têtes, cachets, formules), conventions de
nommage, stratégie de classification, pièges classiques. **Utilise-les activement
pour distinguer les types proches** (ex. DT vs DICT, Devis EPA vs Devis Enviro,
Titre de propriété vs Attestation de vente, CU opérationnel vs CU d'information).
Ces fiches sont INDICATIVES — ne rejette pas un document cohérent si un détail
(dossier, extension, nommage) diffère.

{enriched}

---
"""

    return f"""Tu es un expert en analyse de documents juridiques et techniques liés aux projets photovoltaïques agrivoltaïques en France.

Voici la liste EXHAUSTIVE des types de documents possibles dans un dossier projet EnerVivo :

{types_list}
- Autre / Non identifié{hint_paragraph}

Pour chaque extrait que je te donne, identifie le type le plus probable parmi cette liste.

Règles strictes :
1. Réponds UNIQUEMENT en JSON valide avec exactement trois clés : "type", "confidence", "reason".
2. "type" doit être copié EXACTEMENT depuis la liste ci-dessus (sans paraphrase, sans préfixe, sans les parenthèses d'indice). Si aucun ne convient, mets "Autre / Non identifié".
3. "confidence" est un entier de 0 à 100 reflétant ta certitude :
   - ≥ 80 : signature/cachet/référence officielle visible, contenu sans ambiguïté
   - 60-79 : contenu correspond au type mais éléments de signature manquants
   - 40-59 : indices faibles, plusieurs candidats possibles, version draft
   - < 40 : doute majeur ou document hors périmètre
   ⚠️ Ne baisse PAS la confidence juste parce que le fichier est rangé dans un dossier
   différent du dossier de référence V2 — les vrais projets s'organisent librement.
4. "reason" : UNE phrase en français justifiant le choix (max 25 mots).
5. Ne mets jamais de markdown, jamais de texte hors JSON, jamais d'explication avant ou après.

Exemple de réponse correcte :
{{"type": "PDB signee", "confidence": 92, "reason": "Acte intitulé Promesse de Bail signé par bailleur et preneur avec parcelles cadastrales identifiées."}}
{descriptions_block}"""


def build_user_prompt(file_name: str, text_sample: str, file_path: str | None = None) -> str:
    path_block = f"Chemin SharePoint : {file_path}\n" if file_path else ""
    return f"""Nom du fichier : {file_name}
{path_block}
Extrait du contenu :
\"\"\"
{text_sample}
\"\"\"

Identifie le type de ce document."""


def build_user_prompt_vision(file_name: str, file_path: str | None = None) -> str:
    """Prompt utilisateur pour les PDF scannés (sans couche texte).

    Les images des pages sont jointes en multimodal. Le LLM doit lire les
    titres / cachets / signatures visibles pour classer le document.
    """
    path_block = f"Chemin SharePoint : {file_path}\n" if file_path else ""
    return f"""Nom du fichier : {file_name}
{path_block}
Ce PDF est un SCAN sans couche texte extractible. Les pages t'ont été jointes en images.
Lis le titre, l'en-tête, les cachets et les signatures pour identifier le type.

Identifie le type de ce document."""
