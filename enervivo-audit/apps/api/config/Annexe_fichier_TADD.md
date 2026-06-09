## Classification des TADD par jalon (patterns de nommage)

**Rappel** : contrairement aux Plans de Masse, le jalon est **souvent explicite dans le nom du fichier TADD**. La classification repose en priorité sur cette information. **Un fichier TADD sans notation de jalon dans le nom ne doit PAS être classé.** Ne jamais tenter de deviner le jalon par d'autres indices.

---

### Étape 1 — Identifier les fichiers TADD

Sont considérés comme fichiers TADD tous les fichiers réunissant les deux conditions :
- le mot `TADD` apparaît dans le nom (insensible à la casse)
- l'extension est `.xlsm` ou `.xlsb`

Sont ignorés : les `.xlsx` simples, les PDF, les fichiers sans `TADD` dans le nom.

---

### Étape 2 — Détecter le jalon dans le nom du fichier

Rechercher dans le nom de fichier (insensible à la casse) l'un des tokens de jalon suivants :

| Token recherché | Jalon | Notes |
|-----------------|-------|-------|
| `J1` | **J1** | |
| `J2A` ou `J2a` | **J2a** | |
| `J2B` ou `J2b` | **J2b** | |
| `J3` | **J3** | |
| `J4` | **J4** | |

**Règle de détection robuste** : un token de jalon est valide dès lors qu'il est **délimité de chaque côté** par l'un des caractères suivants : `_`, `.`, `-`, ` ` (espace), ou la fin du nom de fichier (avant l'extension). Cette règle évite les faux positifs (ex : `J10` ne doit pas être détecté comme `J1`).

Exemples de tokens valides dans un nom de fichier :
```
260515_TADD v6.6.10_DGAYRIN_J1_SDU.xlsm   → "_J1_"    ✓
250909_TADD_v6_6_DVAUJANY_J2B_JSW.xlsm    → "_J2B_"   ✓
251120_TADD_v6_6_DDENIS_J3.xlsm           → "_J3."    ✓ (fin de nom)
260102_TADD-v5-DDENIS-J4-VMA.xlsb         → "-J4-"    ✓ (tirets)
240923_TADD_v6_DIBOSH_HBA.xlsb            → aucun     ✗ non classé
```

**Règle absolue : si aucun token de jalon n'est détecté → le fichier est marqué "Non classé" et exclu de la sélection. Ne pas chercher d'autres indices.**

---

### Étape 3 — Départager plusieurs TADD du même jalon

Si plusieurs fichiers TADD portent le même jalon, appliquer les règles suivantes **dans l'ordre strict** :

#### Règle 1 — Version interne la plus haute (priorité absolue)

Le numéro de version (`v...`) désigne la **version interne du modèle TADD VivEpic**, indépendante du jalon. Il peut utiliser des `.` ou des `_` comme séparateurs internes — les normaliser avant de comparer.

**Normalisation** : remplacer tous les `.` et `_` du numéro de version par des `.`, puis lire comme un tuple de nombres entiers.

| Forme dans le nom | Après normalisation | Tuple |
|-------------------|---------------------|-------|
| `v6.6.10` | `v6.6.10` | (6, 6, 10) |
| `v6_6_10` | `v6.6.10` | (6, 6, 10) |
| `v6.6` ou `v6_6` | `v6.6` | (6, 6) |
| `v6` | `v6` | (6,) |
| `v5` | `v5` | (5,) |

**Comparaison** : comparer les tuples composante par composante (comme un numéro de version logiciel). La version la plus haute gagne :
`v6.6.10` > `v6.6` = `v6_6` > `v6` > `v5`

#### Règle 2 — Date de modification système la plus récente (si même version)

Si deux fichiers ont exactement le même numéro de version (après normalisation), sélectionner celui dont la **date de dernière modification** (propriété système du fichier) est la plus récente.

#### Règle 3 — Date encodée dans le nom la plus récente (dernier recours)

Les 6 premiers chiffres du nom encodent une date au format `YYMMDD` (ex : `260515` = 15 mai 2026). Sélectionner le fichier avec la **date la plus récente** dans le nom.

---

### Étape 4 — Output attendu

Pour chaque jalon, produire une ligne de résultat sous la forme :

```
J1  → [nom du fichier retenu]         (motif de sélection si départage)
J2a → [nom du fichier retenu]
J2b → Absent
J3  → [nom du fichier retenu]
J4  → Absent

Non classés (sans jalon dans le nom) :
  - [nom du fichier 1]
  - [nom du fichier 2]
```

- **Présent** : indiquer le nom de fichier retenu et, s'il y avait plusieurs candidats, la règle ayant tranché (ex : "version v6.6.10 > v6.6").
- **Absent** : aucun fichier TADD avec ce jalon trouvé dans le dossier.
- **Non classés** : lister tous les fichiers TADD sans notation de jalon, sans les ignorer silencieusement.

---

### Résumé algorithmique

```
POUR chaque jalon dans [J1, J2a, J2b, J3, J4] :

  candidats = fichiers TADD (.xlsm / .xlsb) dont le nom contient
              le token jalon délimité par [_ . - espace fin-de-nom]

  SI candidats est vide :
    → résultat = Absent

  SI candidats contient 1 fichier :
    → résultat = ce fichier

  SI candidats contient plusieurs fichiers :
    1. Normaliser les versions (remplacer _ par . dans vX...)
    2. Garder celui avec la version la plus haute
    3. Égalité → garder la date de modification système la plus récente
    4. Égalité → garder le YYMMDD du nom le plus récent
    → résultat = fichier retenu + motif

Non classés = fichiers TADD sans aucun token de jalon détecté
```

---

### ⚠️ Pièges à éviter

1. **Ne pas classer un TADD sans jalon explicite** : `TADD_v6_6_DIBOSH_HBA.xlsb` sans token de jalon est "Non classé", même si c'est le seul fichier du dossier.

2. **Ne pas confondre version et jalon** : `v6_6` est la version du modèle, `J2B` est le jalon. Ils coexistent dans le nom sans lien ent