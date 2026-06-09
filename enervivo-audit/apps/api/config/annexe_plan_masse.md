## Classification des Plans de Masse par jalon (patterns de nommage)

**Rappel** : le jalon n'est JAMAIS explicite dans le nom du fichier Plan de Masse (pas de `_J1_`, `_J2a_` dans le nom). Il faut utiliser des **indices secondaires** dans le nom pour deviner le jalon.

### Patterns de nommage observés

| Pattern dans le nom | Jalon probable | Logique |
|---------------------|----------------|---------|
| `_APS_` | **J1** | APS = Avant-Projet Sommaire = version la plus précoce |
| `_APD_` | **J2a** | APD = Avant-Projet Détaillé = affinage post-J1 |
| `_depot_PC_` ou `_PC0_` ou `_DP_` | **J2b** | Version jointe au dépôt du Permis de Construire ou Déclaration Préalable |
| `_EXE_` ou `_PRO_` | **J3 ou J4** | Phase Exécution ou Projet = versions finales pré-construction |

### ⚠️ Les indices de révision (`Ind A`, `Ind B`, `Ind C`...) ne correspondent PAS aux jalons

Les indices A, B, C, D, E sont simplement des **marqueurs chronologiques de révisions** du plan, indépendants des jalons :
- `Ind A` = première version du plan (peut être à n'importe quel jalon)
- `Ind B` = deuxième version (révision)
- `Ind C`, `Ind D`, `Ind E`... = révisions ultérieures

**Exemple** : un projet peut avoir un plan `Ind A` en J1, puis un autre plan `Ind A` en J2b (première version du plan de cette phase). Les indices redémarrent ou continuent selon la convention du BE.

### Stratégie si nom ambigu (pas d'indices ci-dessus)

1. **Trier par date** : le plan le plus ancien = J1, les suivants = J2a, J2b, J3, J4 par ordre chronologique
2. **Chercher dans un dossier `old/` ou `0 - OLD/`** : les versions J1/J2a peuvent y être archivées après comités suivants
3. **Comparer les indices de révision** : `Ind A` < `Ind B` < `Ind C` → ordre chronologique (mais pas de lien direct avec jalon)
4. **En dernier recours** : ouvrir le PDF et lire le cartouche (Phase + date de modification)

### Exemple pratique

- `250520_DDenis_Plan_Masse_APS_Ind_A_VMA.pdf` → **J1** (APS explicite)
- `250820_DDenis_Plan_Masse_APD_Ind_B_VMA.pdf` → **J2a** (APD explicite)
- `251015_DDenis_Plan_Masse_depot_PC_Ind_C_VMA.pdf` → **J2b** (dépôt PC explicite)
- `251210_DDenis_Plan_Masse_EXE_Ind_A_VMA.pdf` → **J3 ou J4** (EXE explicite, Ind A car première version EXE)
