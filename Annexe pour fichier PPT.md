## Classification des dossiers de qualification par jalon (patterns de nommage)

**Rappel** : le dossier de qualification est un fichier PowerPoint (`.pptx`) qui synthétise l'ensemble des pièces BE et développement avant un passage en comité VivEpic. **Le jalon est déterminé uniquement par la présence d'un token de jalon dans le titre du fichier** — c'est la seule et unique méthode. Tout fichier sans notation de jalon dans le nom est **inclassable** et ne doit pas être retenu.

---

### Étape 1 — Identifier les fichiers dossier de qualification

Sont considérés comme dossiers de qualification tous les fichiers réunissant les deux conditions :
- le mot `qualification` apparaît dans le nom (insensible à la casse)
- l'extension est `.pptx` ou `.ppt`

Sont ignorés : les PDF, les fichiers `.xlsx`, tout fichier sans le mot `qualification` dans le nom.

---

### Étape 2 — Détecter le jalon dans le nom du fichier

Rechercher dans le nom de fichier (insensible à la casse) l'un des tokens de jalon suivants :

| Token recherché | Jalon |
|-----------------|-------|
| `J1` | **J1** |
| `J2A` ou `J2a` | **J2a** |
| `J2B` ou `J2b` | **J2b** |
| `J3` | **J3** |
| `J4` | **J4** |

**Règle de détection robuste** : un token de jalon est valide dès lors qu'il est délimité de chaque côté par l'un des caractères suivants : `_`, `.`, `-`, ` ` (espace), ou la fin du nom de fichier (avant l'extension). Cette règle évite les faux positifs (ex : `J10` ne doit pas être détecté comme `J1`).

Exemples de tokens valides :
```
260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx   → "_J2b_"    ✓
260610_DDENIS_qualification_J1_VMA.pptx               → "_J1_"     ✓
260101_DMONFLANQUIN_qualification_J3.pptx             → "_J3."     ✓ (fin de nom)
2025-07-22_DVAUJANY_dossier_qualification_J2a_JSW.pptx → "_J2a_"  ✓
DDENIS_qualification_VMA.pptx                          → aucun     ✗ inclassable
DIBOSH_Modèle_qualification_projetS21_HBA.pptx         → aucun     ✗ inclassable
```

**Règle absolue : si aucun token de jalon n'est détecté → le fichier est marqué "Non classé" et exclu de la sélection. Ne jamais chercher d'autres indices (contenu du fichier, date seule, etc.).**

---

### Étape 3 — Départager plusieurs dossiers du même jalon

Si plusieurs fichiers portent le même jalon, appliquer les règles suivantes **dans l'ordre strict** :

#### Règle 1 — Date encodée dans le nom la plus récente (priorité absolue)

Les premiers chiffres du nom encodent une date au format `YYMMDD` (ex : `260305` = 5 mars 2026) ou `YYYY-MM-DD` (ex : `2025-07-22`). Sélectionner le fichier avec la **date la plus récente** dans le nom.

```
260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx    → 05/03/2026
260310_DVAUJANY_dossier_qualification_J2b_VMA.pptx    → 10/03/2026  ← retenu
```

#### Règle 2 — Date de modification système la plus récente (cas critique)

Si deux fichiers ont exactement la même date encodée dans le nom, sélectionner celui dont la **date de dernière modification** (propriété système du fichier) est la plus récente.

---

### Étape 4 — Output attendu

Pour chaque jalon, produire une ligne de résultat sous la forme :

```
J1  → [nom du fichier retenu]         (motif de sélection si départage)
J2a → [nom du fichier retenu]
J2b → Absent
J3  → [nom du fichier retenu]
J4  → Absent

Non classés (sans notation de jalon dans le nom) :
  - [nom du fichier 1]
  - [nom du fichier 2]
```

- **Présent** : indiquer le nom de fichier retenu et, s'il y avait plusieurs candidats, la règle ayant tranché (ex : "260310 > 260305" ou "date de modification 15/04 > 10/03").
- **Absent** : aucun dossier de qualification avec ce jalon trouvé dans le dossier.
- **Non classés** : lister tous les fichiers `qualification` sans notation de jalon — ne jamais les ignorer silencieusement.

---

### Résumé algorithmique

```
POUR chaque fichier .pptx / .ppt dont le nom contient "qualification" :

  Chercher token jalon [J1, J2a, J2b, J3, J4]
  délimité par [_ . - espace fin-de-nom]

  SI aucun token → Non classé (fin, ne pas traiter davantage)
  SI token trouvé → candidat pour ce jalon

POUR chaque jalon dans [J1, J2a, J2b, J3, J4] :

  SI candidats est vide :
    → résultat = Absent

  SI candidats contient 1 fichier :
    → résultat = ce fichier

  SI candidats contient plusieurs fichiers :
    1. Extraire la date du nom (YYMMDD ou YYYY-MM-DD)
    2. Garder celui avec la date la plus récente
    3. Égalité → garder la date de modification système la plus récente
    → résultat = fichier retenu + motif

Non classés = fichiers "qualification" sans token de jalon détecté
```

---

### ⚠️ Pièges à éviter

1. **Ne pas classer un fichier sans jalon explicite** : `DIBOSH_Modèle_qualification_projetS21_HBA.pptx` sans token de jalon est "Non classé", même si c'est le seul fichier du dossier.

2. **Faux positif sur J1** : vérifier que le token n'est pas `J10`, `J11`, etc. La règle de délimitation (caractère séparateur de chaque côté) protège contre ce cas.

3. **Ne pas confondre J2a et J2b** : `J2A`/`J2a` et `J2B`/`J2b` sont proches — lire attentivement. `J2b` est la version dépôt PC, `J2a` est la version pré-dépôt.

4. **Format de date variable** : `260305` (YYMMDD) et `2025-07-22` (YYYY-MM-DD avec tirets) désignent tous deux une date — extraire les chiffres dans les deux cas pour comparer.

5. **Fichiers dans des sous-dossiers `old/` ou `0 - OLD/`** : ne pas les ignorer automatiquement. Si c'est le seul fichier disponible pour un jalon (avec token valide), il est retenu. Appliquer les mêmes règles de départage.

---

### Exemples pratiques

**Cas 1 — Département simple :**
```
Fichiers :
  260610_DDENIS_dossier_qualification_J1_VMA.pptx
  2025-07-22_DVAUJANY_dossier_qualification_J2a_JSW.pptx
  260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx
  260310_DVAUJANY_dossier_qualification_J2b_VMA.pptx
  DIBOSH_Modèle_qualification_projetS21_HBA.pptx

Résultat :
  J1  → 260610_DDENIS_dossier_qualification_J1_VMA.pptx
  J2a → 2025-07-22_DVAUJANY_dossier_qualification_J2a_JSW.pptx
  J2b → 260310_DVAUJANY_dossier_qualification_J2b_VMA.pptx   (260310 > 260305)
  J3  → Absent
  J4  → Absent
  Non classés : DIBOSH_Modèle_qualification_projetS21_HBA.pptx
```

**Cas 2 — Même date, départage par modification système :**
```
Fichiers :
  260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx   (modifié le 10/03/2026)
  260305_DVAUJANY_dossier_qualification_J2b_VMA.pptx   (modifié le 15/03/2026)

Résultat :
  J2b → 260305_DVAUJANY_dossier_qualification_J2b_VMA.pptx
        (même date 260305 → date de modification 15/03 > 10/03)
```
