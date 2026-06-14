"""Garde-fou : ramène un `type` LLM hors-référentiel vers un type V12 valide.

Problème observé après bascule sur Gemini Flash-Lite (petit modèle, adhérence
imparfaite aux contraintes) : le LLM **invente** des types absents du référentiel
V12, malgré la règle « copie EXACTEMENT depuis la liste ». Exemples DIBOS_H :
  - « Avis de situation au Répertoire SIRENE INSEE » → en réalité « Extrait Kbis »
  - « CDB signee »                                  → en réalité « Statuts SPV signes »
  - « Devis Enviro »                                → « Devis signé Enviro » (variante)
Ces types inventés cassent le matcher (normalize-exact) → fichier en unclassified.

Stratégie (décidée avec l'utilisateur) :
  1. Type déjà valide (== un type V12 après normalisation) → inchangé.
  2. Alias métier explicite connu → type V12 cible.
  3. Sinon, snap au type V12 le plus proche SI la similarité est forte
     (préfixe/inclusion + ratio élevé) — couvre les variantes orthographiques.
  4. Sinon → « Autre / Non identifié » (le BE tranche ; jamais de faux mapping).

Déterministe, indépendant du modèle, attrape aussi les futurs types inventés.
"""

from __future__ import annotations

import unicodedata
from typing import Any

# Type fourre-tout du référentiel. Exposé en public (OTHER_TYPE) car c'est un
# contrat partagé : la passe 2 TADD y bascule les versions écartées.
OTHER_TYPE = "Autre / Non identifié"
_OTHER = OTHER_TYPE

# Types HORS-référentiel mais LÉGITIMES, posés volontairement par une passe 2.
# Ils ne doivent JAMAIS être snappés (sinon "TADD (non classé)" relu depuis le
# cache deviendrait "Autre / Non identifié" → perte de l'étiquette TADD voulue).
# La passe 2 TADD utilise ce libellé pour un TADD sans token de jalon dans le
# nom (annexe : "Non classé, exclu de la sélection, ne pas deviner").
TADD_UNCLASSIFIED_TYPE = "TADD (non classé)"
# Idem pour les dossiers de qualification sans token de jalon dans le nom
# (annexe PPT : "Non classé, exclu de la sélection, ne pas deviner").
QUALIF_UNCLASSIFIED_TYPE = "Dossier de qualification (non classé)"
_PROTECTED_TYPES = frozenset({TADD_UNCLASSIFIED_TYPE, QUALIF_UNCLASSIFIED_TYPE})

# Snap par INCLUSION DE TOKENS plutôt que par ratio de similarité global.
# Un type inventé est rapproché d'un type V12 SSI TOUS ses mots significatifs
# (≥ _MIN_TOKEN_LEN) sont présents dans le type V12 candidat. Logique :
#   - « Devis Enviro » ⊂ « Devis signé Enviro » → tous les mots de l'inventé
#     sont dans le candidat → SNAP ✅
#   - « DICT DT résumé » vs « DICT DICT résumé » → le mot « DT » n'est PAS dans
#     le candidat → PAS de snap → Autre ✅ (DT ≠ DICT, docs distincts)
# Évite la tension d'un seuil de ratio unique (trop bas = faux DT/DICT, trop
# haut = variantes ratées). En cas de PLUSIEURS candidats éligibles → ambigu →
# Autre (on ne devine pas).
_MIN_TOKEN_LEN = 2  # ignore les mots de 1 lettre (bruit), garde « dt », « pv »…

# Alias métier EXPLICITES : équivalences que le référentiel EnerVivo accepte
# mais que le LLM nomme autrement. Clé = forme normalisée du type inventé,
# valeur = nom V12 EXACT cible. Confirmés par la vérité-terrain V12 (Lien_*).
_ALIASES_NORM: dict[str, str] = {
    # Sociétés agricoles (SCEA/EARL/GAEC) : pas de Kbis RCS → avis SIRENE INSEE
    # est la source officielle. V12 #21 attend bien le fichier SIRENE en Kbis.
    "avis de situation au repertoire sirene insee": "Extrait Kbis a jour (proprio personne morale)",
    "avis de situation sirene insee": "Extrait Kbis a jour (proprio personne morale)",
    "avis sirene insee": "Extrait Kbis a jour (proprio personne morale)",
    # Courrier de substitution (art. 8 PDB) : V12 #55 le mappe sur Statuts SPV.
    "cdb signee": "Statuts SPV signes",
}


_DASH_VARIANTS = "‐‑‒–—―−­"


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or ""))
    for d in _DASH_VARIANTS:
        s = s.replace(d, " ")
    s = s.encode("ascii", "ignore").decode("ascii")
    return " ".join(s.lower().split())


def _valid_types(reference: dict[str, Any]) -> dict[str, str]:
    """{forme normalisée -> nom V12 exact}. Inclut « Autre / Non identifié »."""
    out: dict[str, str] = {}
    for jalon in reference.get("jalons", []):
        for doc in jalon.get("documents", []):
            name = doc.get("name")
            if name:
                out[_norm(name)] = name
    out[_norm(_OTHER)] = _OTHER
    return out


def snap_type_to_referential(type_value: str, reference: dict[str, Any]) -> str:
    """Renvoie un type V12 valide. Voir docstring module pour la stratégie."""
    # 0. Types hors-référentiel protégés (posés sciemment par une passe 2) :
    #    renvoyés VERBATIM, jamais snappés. Sinon "TADD (non classé)" relu
    #    depuis le cache tomberait en "Autre" (token "tadd" ⊄ un seul type) →
    #    perte de l'étiquette voulue.
    if (type_value or "").strip() in _PROTECTED_TYPES:
        return type_value.strip()

    valid = _valid_types(reference)
    n = _norm(type_value)

    # 1. Déjà valide → on renvoie le nom V12 exact (corrige aussi accents/casse).
    if n in valid:
        return valid[n]

    # 2. Alias métier explicite.
    if n in _ALIASES_NORM:
        target = _ALIASES_NORM[n]
        # Sécurité : l'alias doit pointer vers un type réellement présent.
        if _norm(target) in valid:
            return valid[_norm(target)]

    # 3. Snap par inclusion de tokens : un candidat V12 est éligible si TOUS les
    #    mots significatifs du type inventé y figurent. Si exactement UN candidat
    #    est éligible → snap. Si zéro ou plusieurs (ambigu) → Autre.
    inv_tokens = {t for t in n.split() if len(t) >= _MIN_TOKEN_LEN}
    if inv_tokens:
        eligible = []
        for norm_name, exact in valid.items():
            if exact == _OTHER:
                continue
            cand_tokens = set(norm_name.split())
            if inv_tokens <= cand_tokens:  # tous les mots de l'inventé ∈ candidat
                eligible.append(exact)
        if len(eligible) == 1:
            return eligible[0]

    # 4. Rien de fiable (zéro ou plusieurs candidats) → Autre (le BE tranche).
    return _OTHER
