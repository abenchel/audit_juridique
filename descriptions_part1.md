# Descriptions enrichies — Référentiel documents par jalon VivEpic

**Version** : V12 (draft 1)
**Source** : référentiel V11 (260518_Document_par_Jalon_V11.xlsx) + analyse de vrais exemples uploadés
**Usage** : input pour LLM classifier de l'app POC Audit Juridique
**Langue** : FR, français administratif métier
**Format** : chaque description suit la structure : définition métier → format observé → indices internes typiques → nommage observé → stratégie de classification → pièges

---

## 📋 Convention de nommage générale VivEpic (à intégrer au prompt système du LLM)

**Format standard** : `YYMMDD_[CodeProjet]_[TypeDoc]_[Métadonnées]_[TRIGRAMME].[ext]`

- **YYMMDD** au début = date de création/modification
- **CodeProjet** = code court (DDENIS, DVAUJANY, DIBOSH, DMARIE1, DMONFLANQUIN, RJARGAR…). Préfixe `D` = projet en Développement, `R` = projet en Repowering
- **TypeDoc** = nom du document (Plan_Masse, TADD, dossier_qualification…)
- **Métadonnées** = jalon (J1, J2a, J2b…), version interne (Ind A, v6_6…), phase technique (APS, APD, EXE…)
- **TRIGRAMME** = initiales du PM (non utilisé pour classification métier — décision Julien)

Convention **utile mais pas toujours respectée** (anciens projets, fichiers reçus de tiers).

---

## Légende propriétés

- **Obligatoire** : doit être présent pour valider le jalon
- **Cas par cas** : présent uniquement si projet le déclenche
- **Facultatif** : présent selon contexte, n'empêche pas la validation
- **Annexes 3 PDB** : pièces justificatives listées en Annexe 3 de la Promesse de Bail (à fournir par le Promettant)

## Légende versioning

- **Document unique** : un seul exemplaire, valide une fois
- **Version signée uniquement** : drafts ignorés, seule la version signée des parties compte
- **Versionné par jalon** : un exemplaire par jalon (J1, J2a, J2b…), tous coexistent

---

# AVANT J1 — Qualification

## 1. LOI signée

- **Jalon** : Avant J1
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

* [ ] Lettre d'Intention signée par le propriétaire foncier et VivEpic/EnerVivo, formalisant l'accord de principe pour étudier le projet photovoltaïque sur ses parcelles. Document précédant la PDB.

**Format observé** : souvent **uniquement la dernière page** scannée ou photographiée (PDF/JPG/PNG d'1 page), contenant la phrase type "Proposition pour signature d'une promesse de bail", les conditions économiques chiffrées (€/MWc/an, durée 40 ans, surface en hectares), et **les deux signatures manuscrites** (propriétaire + représentant EnerVivo).

**Indices internes typiques** :

- Mentions "EnerVivo" et "promesse de bail emphytéotique"
- Conditions financières : montant en €/MWc/an (souvent 2500€), durée (40 ans)
- "Fait à [commune], le [date]/2025"
- Note "Offre valable 2 mois"
- Signatures manuscrites du propriétaire ET d'EnerVivo (les deux requises)

**Nommage** : `LOI_[NomProprio]_[date].pdf` (ex : `LOI_Millet_du_05_02_25.pdf`). Souvent dans `4-Documents Administratifs/LOI` ou équivalent.

**Piège** : ne pas confondre avec un draft non signé. Si une seule signature ou aucune → ce n'est PAS une LOI valide pour validation jalon.

---

# J1 — Validation comité VivEpic

## 2. PDB signée

- **Jalon** : J1
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

Promesse de Bail Emphytéotique signée entre le propriétaire foncier (le "Promettant") et EnerVivo (le "Bénéficiaire"), souvent contre-signée par avocat. **La signature de ce document vaut validation du jalon J1.**

**Format observé** : PDF de 25-30 pages, en-tête sur chaque page avec logo `EnerVivo` à gauche et mention `PDB_CENTRALE AU SOL` ou `PDB_CENTRALE AU TOIT` à droite (selon le type de projet).

**Indices internes typiques** :

- **Page 1** : "PROMESSE DE BAIL EMPHYTEOTIQUE" en gros titre, "ENTRE LES SOUSSIGNES", identification du Promettant (nom, date de naissance, adresse, régime matrimonial)
- **Page 2-3** : Table des matières structurée en 11 Articles + 6 Annexes
- **Articles clés** : Article 1 (Objet), Article 2 (Durée — typiquement 48 mois), Article 3 (Conditions suspensives), Article 4 (Exclusivité), Article 6 (Obligations des parties), Article 8 (Résiliation)
- **Section finale** : "Fait à [ville], le [date]", "En deux exemplaires originaux", **signatures manuscrites du Promettant ET du Bénéficiaire (EnerVivo, représenté par Sylvain FREDERIC ou autre habilité)**
- **Annexes** : Annexe 1 (Plan cadastral), Annexe 2 (Désignation parcelles), Annexe 3 (Pièces justificatives — les 11 pièces PDB), Annexe 4 (Termes du bail), Annexe 5 (Terrassement), Annexe 6 (Mandat dépôt urbanisme)

**Nommage observé** : `YYYY-MM-DD Promesse bail emphytéotique - [NomProprio] - signée-courrier.pdf` ou `PDB_signée.pdf`.

**Localisation** : `4 - Documents Administratifs/Promesse de Bail` ou `6-Bail`.

**Piège majeur** : drafts à ignorer absolument — seule la version avec les 2 signatures manuscrites sur la dernière page d'articles (avant les annexes) est valide. Si annexes vides ou non-paraphées par le propriétaire → version partielle.

---

## 3. Plan de masse version J1

- **Jalon** : J1
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Plan d'implantation 2D de la centrale photovoltaïque sur les parcelles, dans sa **version au moment du comité J1** (la plus précoce — souvent qualifiée d'APS, "Avant-Projet Sommaire").

**Format observé** : PDF (souvent extrait depuis AutoCAD format A3), comportant typiquement **plusieurs folios** (1/5 à 5/5) avec cartouche EnerVivo en bas à droite. Possible aussi `.dwg`.

**🚨 Difficulté principale** : **le nom du fichier ne contient JAMAIS le jalon** ("J1", "J2a" ne sont pas dans le nom). Il faut donc s'appuyer sur **les indices internes**.

**Indices internes pour identifier le jalon** :

- **Cartouche en bas à droite** : ligne `Phase : APS` (= J1) / `APD` (= J2a/J2b) / `EXE` (= J3-J4)
- **Indice de révision** : `Ind A` = première version (typiquement J1) / `Ind B`, `Ind C`, etc. = révisions ultérieures (jalons suivants)
- **Cartouche "Modification"** : ligne `APS A 22/05/2025 Création plan` indique la création (J1). Présence de plusieurs lignes de modifs = jalons ultérieurs.
- **Caractéristiques techniques préliminaires** : valeurs `xxxx` ou `--X` non encore renseignées (P50, P90, modèle d'onduleur incomplet) → indice fort d'une version J1

**Indices internes communs (peu importe le jalon)** :

- Logo EnerVivo, adresse "185 Boulevard Maréchal Leclerc 33000 Bordeaux"
- Cartouche : `Projet : [CODE]`, `Phase :`, `Echelle`, `Folio X/Y`, `Ind`, `Date`, `Nom de la Commune`, `Code postal`, `Parcelles cadastrales`
- Caractéristiques techniques : nombre de modules, Pdc en MWc, modèle module (ex : Jinko Solar 645Wc biface), surface projetée
- Légende standardisée : panneaux PV, clôtures, pistes, citerne SDIS, PDL/TR, PTR, BI…

**Nommage observé** : `YYMMDD_[CodeProjet]_Plan_Masse_Ind_[X]_[TRIGRAMME].pdf` (ex : `250520_DDenis_Plan_Masse_Ind_A_VMA.pdf`). Souvent dans `6 - Techniques/Plans/Plan de masse`.

**Stratégie de classification jalon** :

1. Si `Ind A` ET `Phase : APS` ET date proche du comité J1 → **Plan de masse J1**
2. Si plusieurs versions existent dans le dossier : la **plus ancienne (date la plus précoce)** est le J1, les suivantes correspondent à J2a/J2b/J3/J4
3. Si dossier contient sous-dossier `old/` ou `0 - OLD/` : la version J1 peut s'y trouver après les comités suivants

---

## 4. TADD version J1

- **Jalon** : J1
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

**Tableau d'Analyse Détaillée des Données** — c'est le **business plan financier** du projet sous forme de fichier Excel avec macros, dans sa version au comité J1 (hypothèses préliminaires).

**Format observé** : `.xlsm` (Excel avec macros) ou `.xlsb` (Excel binaire) — pas un `.xlsx` simple. Plusieurs onglets de calculs : production estimée (issue PVsyst), CAPEX, OPEX, revenus de vente d'électricité, TRI, VAN, payback.

**🚨 Versionnage interne complexe** :

- **Le numéro `v6_6` ou `v5` dans le nom = version interne du modèle TADD VivEpic**, PAS le jalon
- **Utilité du numéro de version** : il permet de classer les TADD dans l'ordre chronologique de création
- **Le jalon est souvent (mais pas toujours) explicitement dans le nom** : `_J1_`, `_J2A_`, `_J2B_`, `_J3_`, `_J4_`

**Indices internes typiques** :

- Onglets standards : "Hypothèses", "PVsyst" ou "Production", "CAPEX", "OPEX", "Cash-flow", "Synthèse"
- Code projet en première cellule ou onglet
- Cellule indiquant le jalon ("Jalon courant : J1") ou présentation de version dans onglet "Synthèse"
- Macros activées (présence de boutons, formulaires VBA)

**Nommage observé** :

- `YYMMDD_TADD_v[X]_[Y]_[CODEPROJET]_J[X]_[TRIGRAMME].xlsm` (ex : `250909_TADD_v6_6_DVAUJANY_J2B_JSW.xlsm`)
- Variante sans jalon : `2024 09 23 DIBOSH_TADD_v6_HBA.xlsb`

**Localisation** : `3 - TAD` ou `3-TAD`.

**Stratégie de classification jalon (par ordre de fiabilité)** :

1. **Jalon explicite dans le nom** (`_J1_`, `_J2B_`) → fiable
2. **Sinon, chercher dans le fichier** : onglet "Synthèse" ou "Couverture", cellule "Jalon" ou "Stade projet"
3. **Sinon, raisonnement par date** : la version la plus ancienne du dossier est typiquement J1
4. **Sinon, indice par la version interne** : v5 plus probable d'être un J1/J2a que v6_6

---

## 5. Dossier de qualification J1

- **Jalon** : J1
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

**PowerPoint de présentation du projet au comité VivEpic** pour validation du jalon. **Le titre du fichier indique explicitement le jalon** — c'est le seul document de la liste où le jalon est systématiquement explicite dans le nom.

**Format observé** : `.pptx`. Slide deck intégrant : page de garde avec code projet et jalon, contexte foncier, plan de masse, résultats PVsyst, TADD synthétique, enjeux administratifs/techniques.

**Indices internes typiques** :

- **Page de garde** : titre "Dossier de qualification", code projet, jalon explicite ("J1", "J2b"), date, trigramme du PM
- Charte EnerVivo (vert forêt #1C7862, jaune solaire #FFDD00, logo EnerVivo en haut)
- Slides typiques : "Contexte foncier", "Plan de masse", "Étude PVsyst", "Plan d'affaires" / "TADD", "Enjeux", "Planning", "Décision attendue"
- Mention "Comité VivEpic du [date]" en page de garde

**Nommage observé** :

- `YYMMDD_[CODEPROJET]_dossier_qualification_J[X]_[TRIGRAMME].pptx` (ex : `260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx`)
- Variante ancienne : `YYYY MM DD [CODEPROJET]_Modèle_qualification_projetS21_[TRIGRAMME].pptx`

**Localisation** : `2 - Presentations ppt` ou `2-Presentations ppt`.

**Stratégie de classification jalon** :

1. **Jalon explicite dans le nom** → fiable à 95%
2. **Si nom ancien** ("Modèle_qualification_projetS21") : pas de jalon dans le nom → ouvrir le PPT et lire la page de garde

**Piège** : ne pas confondre les versions de jalons différents qui peuvent coexister dans le même dossier.

---

# J2a — Permitting phase A

## 6. Certificat d'urbanisme opérationnel (CU)

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Acte administratif délivré par le **maire au nom de la commune** (ou par la DDT) en application des articles L. 410-1, R. 410-1 du Code de l'urbanisme. **Pour un projet PV : il faut obligatoirement le CU opérationnel (type b) — pas le CU d'information (type a).** Le CU précise les règles d'urbanisme applicables, les taxes, les servitudes, et **certifie si le terrain peut être utilisé pour l'opération envisagée**.

**Format observé** : PDF, document officiel typiquement 4-5 pages.

**Indices internes typiques** :

- **En-tête** : "CERTIFICAT D'URBANISME OPERATIONNEL" en gros titre + "DÉLIVRÉ PAR LE MAIRE AU NOM DE LA COMMUNE"
- **Référence à gauche** : "COMMUNE DE [NOM]"
- **Cartouche dossier** : `DOSSIER N° CU [code INSEE] [Année] [N°]` (ex : `CU 47175 25 B0109`)
- **Champs structurés** : "déposé le", "par" (SAS EnerVivo représentée par Monsieur FREDERIC Sylvain), "sur un terrain sis", "cadastré", "surface", "objet de la demande"
- **Section "CERTIFIE"** avec Articles 1 à 8 numérotés
- **Article 2 clé** : "Le terrain objet de la demande peut être utilisé pour la réalisation de l'opération envisagée" (= validation)
- **Article 8** : liste des formalités à venir (typiquement "Demande de permis de construire")
- **Signature** : "Fait à [commune], le [date]", "Par délégation, Le Maire Adjoint, [Nom]" avec cachet de mairie
- Mention "Décision notifiée au demandeur le ..."
- Pied de page récurrent : "DOSSIER N° CU [...]" + numérotation PAGE X/Y

**Nommage observé** : `CU_[INSEE]_[AA]_B[N°]-arrete_decision_[X]_[Y].pdf` (ex : `CU_47175_25_B0109-arrete_decision_1_1.pdf`).

**Localisation** : `4 - Documents Administratifs/Certificat urbanisme` ou `7-Urbanisme/CU`.

**Pièges à éviter** :

1. **Ne pas confondre avec un CU d'information (type a)** — chercher absolument "OPERATIONNEL" dans le titre
2. **Ne pas confondre avec la demande de CU** (CERFA 13410, formulaire vide) — on veut **l'arrêté de décision**, pas la demande
3. **Vérifier la validité** : un CU est valable 18 mois — si daté de plus de 18 mois et pas prorogé, il est caduc
4. **Cas "tacite"** : absence de réponse au-delà du délai = CU tacite (pas de document PDF, juste preuve de dépôt + accusé)

---

## 7. Compte-rendu RDV maire et élus

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple — 1 par RDV)

### Description

Note interne EnerVivo synthétisant les échanges lors d'un RDV avec le maire, l'équipe municipale ou des élus locaux (conseillers, adjoints). Document préparatoire pour démontrer la concertation locale. **Peut être multiple : 1 par RDV** (souvent plusieurs RDV avant validation J2a).

**Format observé** : Word (`.docx`) ou PDF, document court 1-3 pages.

**Indices internes typiques** :

- **En-tête** : logo EnerVivo, "Compte-rendu", "Réunion du [date]", lieu (Mairie de [commune])
- **Liste des participants** : élus présents (Maire, Adjoints, conseillers), représentants EnerVivo, parfois propriétaire foncier
- **Sections** : "Objet de la réunion", "Points abordés", "Décisions / Actions à mener", "Prochaines étapes"
- **Sujets typiques** : présentation du projet, contraintes urbanisme, intégration paysagère, retombées économiques, calendrier

**Nommage probable** : `CR_RDV_Mairie_[Commune]_[date].docx`, `Compte-rendu_Mairie_[Commune]_YYYYMMDD.pdf`.

**Localisation** : `4 - Documents Administratifs/Comptes-rendus` ou `Comptes-rendus mairie`.

**Stratégie de classification** :

1. Distinguer du CR Chambre d'Agriculture, EPCI, DDT (tous sont des "CR RDV" mais avec interlocuteur différent) → utiliser **les participants ou l'objet** pour discriminer
2. **Plusieurs CR par projet attendus** : ne pas filtrer sur l'unicité, lister tous les CR avec dates
3. Si format peu structuré (juste notes manuscrites scannées) : possible CR informel — flag pour vérification PM

---

## 8. Compte-rendu RDV EPCI / ComCom

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple)

### Description

Compte-rendu de réunion avec l'Établissement Public de Coopération Intercommunale (communauté de communes ou communauté d'agglomération). Même nature que le CR mairie mais avec un interlocuteur intercommunal. Concerne typiquement le schéma de cohérence territorial (SCoT), les enjeux paysagers à échelle intercommunale, ou la position politique de l'EPCI sur l'ENR.

**Format et indices** : identiques au CR RDV maire. **Discriminant** : les participants mentionnent un président de ComCom, DGS intercommunal, élu EPCI, ou mention explicite "Communauté de communes de [nom]" / "EPCI" / "ComCom" dans l'objet.

**Nommage probable** : `CR_RDV_EPCI_[Commune]_[date]`, `CR_ComCom_[nom]_[date]`.

**Piège** : ne pas confondre avec le CR mairie. Discriminer sur l'interlocuteur (mairie = commune seule, EPCI = échelon intercommunal).

---

## 9. Compte-rendu RDV Chambre d'Agriculture

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple)

### Description

Compte-rendu de réunion avec la Chambre d'Agriculture départementale. Concerne typiquement la compatibilité du projet avec l'activité agricole locale, l'avis de la Chambre sur la compensation agricole, la position sur l'agrivoltaïsme.

**Format et indices** : identiques au CR RDV maire. **Discriminant** : participants mentionnent un représentant de la Chambre d'Agriculture, ou mention explicite "Chambre d'Agriculture [département]" dans l'objet ou les participants.

**Nommage probable** : `CR_RDV_CA_[Dept]_[date]`, `CR_Chambre_Agriculture_[date]`.

**Piège** : ne pas confondre avec le rapport EPA (qui intègre une analyse de la Chambre d'Agriculture mais n'est pas un CR de RDV).

---

## 10. Compte-rendu RDV DDT(M)

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple)

### Description

Compte-rendu de réunion avec la Direction Départementale des Territoires (et de la Mer) — administration qui instruit les autorisations d'urbanisme, les dossiers ICPE, les questions agricoles et environnementales. RDV souvent demandé par EnerVivo pour **pré-cadrer l'instruction** : comprendre la doctrine locale sur l'agrivoltaïsme, les attendus de la CDPENAF, les points de vigilance.

**Format et indices** : identiques aux autres CR. **Discriminant** : participants mentionnent "DDT", "DDTM", "chef de service urbanisme", "pôle ENR de la DDT". Contenu typique : doctrine locale, seuils compensation, dossier type attendu.

**Nommage probable** : `CR_RDV_DDT_[Dept]_[date]`, `CR_DDTM_[Dept]_[date]`.

---

## 11. Feuille d'émargement comité projet

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Document de preuve de tenue d'un comité de projet interne EnerVivo (ou élargi aux partenaires) attestant que les parties prenantes se sont réunies pour valider les orientations du projet. **Peut être hors J2a** (créé à n'importe quel jalon), mais rattaché à J2a dans le référentiel.

**Format observé** : PDF ou scan, typiquement **1 page**, format tabulaire.

**Indices internes typiques** :

- **Titre** : "Feuille d'émargement" ou "Liste de présence" ou "Feuille de présence"
- **Tableau** : colonnes Nom / Prénom / Organisme / Fonction / Signature
- **En-tête** : mention "Comité projet [Code projet]", date de la réunion, lieu
- **Signatures manuscrites** de chaque participant (c'est la preuve de présence physique)
- Peut contenir un logo EnerVivo ou être un simple tableau imprimé

**Nommage probable** : `Feuille_emargement_[date]`, `Emargement_comite_[code projet]`, `Liste_presence_[date]`.

**Localisation** : potentiellement dans `4 - Documents Administratifs/Comptes-rendus` ou à la racine du dossier jalon.

**Piège** : ne pas confondre avec un CR de réunion (le CR a du contenu rédactionnel, la feuille d'émargement est juste un tableau de signatures). Les deux peuvent coexister pour le même comité.

---

## 12. Devis signé EPA

- **Jalon** : J2a
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

**Devis / Proposition Technique et Financière (PTF)** signé par EnerVivo auprès d'un bureau d'études agricole et environnemental, marquant le lancement officiel de la commande d'EPA. **L'étude elle-même n'est pas attendue en J2a** — c'est uniquement la commande qui valide le jalon. **Version signée des deux parties uniquement (drafts ignorés).**

**Cadre réglementaire** : EPA = obligation issue de la **Loi LAAAF du 13 octobre 2014** et **décret n° 2016-1190 du 31 août 2016** (compensation agricole collective). Obligatoire si emprise > 5 ha en zone agricole.

**Format observé** : PDF d'environ 20-30 pages, livré par le BE prestataire (souvent Artifex / Socotec Aménagement Biodiversité, mais d'autres BE possibles).

**Indices internes typiques** :

- **Page de garde** : logo du BE prestataire (Artifex/Socotec, Naldéo, Agroconsult, etc.) + logo EnerVivo + titre "Etude Préalable Agricole — Proposition technique et financière" + référence type `2025-XXXX` + commune et département du projet + date
- **Mention "Centrale ENERVIVO" ou "ENERVIVO" en client**, adresse 185 Boulevard Maréchal Leclerc 33000 Bordeaux
- **Sommaire structuré** : "Fiche de synthèse", "Cadre de référence" (mentions du **Décret n° 2016-1190** et/ou **Décret du 8 avril 2024 agrivoltaïsme**), "Votre demande", "Notre prestation", "Équipe projet", "Références", "Proposition financière", "Bon de commande"
- **Partie 1 - Fiche de synthèse** : tableau client (Thomas GUERIN, Sylvain FREDERIC ou autre contact EnerVivo), bureau d'études, localisation projet, surface, **Montant offre de base en € HT**
- **Cadre réglementaire** : mention du Décret 2016-1190, article L. 112-1-3 du Code rural, CDPENAF
- **Partie 7 - Proposition financière** : tableaux détaillés HT/TTC, prestations de base + optionnelles (Note technique APER, étude agropédologique)
- **Partie 8 - Bon de commande** : tableau des prestations + cases "Validation client" cochées + cadre **signature avec mention "Lu et accepté"** + tampon **"Certifié par YouSign"** (signature électronique) + nom et signature manuscrite/électronique de **Sylvain FREDERIC** ou autre habilité EnerVivo
- **Mention de validation explicite** : ex. "Lu et approuvé. Validation de la PRESTATION OPTIONNELLE N°1 uniquement"
- **Échéancier de facturation** : tableau avec acomptes (20% à la commande, etc.)

**Nommage observé** : `PTF_[BE]_ENERVIVO_EPA_[Mentions]_[Commune]_[Dept]_[YYYYMMDD]_signed_.pdf` (ex : `PTF_ARTIFEX_ENERVIVO_EPA_APER_Agropedo_AgriPV_Uzein_64_20251119__signed_.pdf`). Le suffixe **`_signed_`** dans le nom est un indicateur très fort de signature YouSign.

**Localisation** : `7 - Achat-Fournisseurs/1-Consultations/EPA` ou équivalent. Souvent rangé par fournisseur.

**Pièges à éviter** :

1. **Drafts non signés à ignorer** : si absence du tampon YouSign ET pas de signature manuscrite → ce n'est PAS un devis signé valide pour le jalon
2. **Ne pas confondre avec le rapport EPA final** (livrable de l'étude, attendu en J2b) : le devis fait 20-30 pages, le rapport final fait 100-200+ pages
3. **Ne pas confondre avec un devis Enviro** : le devis EPA mentionne spécifiquement "Étude Préalable Agricole", Décret 2016-1190, CDPENAF
4. **Mention "Cas par cas" en propriété** : devis EPA obligatoire seulement si emprise > seuil départemental (1-10 ha, défaut 5 ha) — pour petits projets, peut être absent (N/A)

---

## 13. Devis signé Enviro

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

Devis / PTF signé par EnerVivo auprès d'un bureau d'études environnemental, **regroupant typiquement les commandes EIE / VNEI / PEDO-ZH / FAUNE et FLORE** sur un même contrat (ou contrats séparés selon le BE). **L'étude elle-même est attendue en J2b** (rapport VNEI saison 1/2, EIE) — en J2a on attend uniquement la commande signée qui matérialise le lancement.

**Sigles métier à connaître** :

- **EIE** : Étude d'Impact Environnemental
- **VNEI** : Volet Naturel de l'Étude d'Impact
- **PEDO-ZH** : étude **pédologique et zones humides**
- **Faune et Flore** : inventaires naturalistes (4 saisons typiquement)

**Format observé** : PDF, structure très similaire au devis EPA (mêmes BE possibles ou BE différents : Biotope, Calidris, Naldéo, Egis Environnement, etc.).

**Indices internes typiques** :

- **Page de garde** : logo BE environnemental + EnerVivo client + titre **"Proposition technique et financière — Étude d'impact"** ou **"VNEI"** ou **"Volet milieu naturel"** ou **"Inventaires faune-flore et zones humides"**
- **Cadre réglementaire** : mention du **Code de l'environnement**, articles **R. 122-2** (étude d'impact systématique), **L. 411-1** (espèces protégées), **L. 211-1** (loi sur l'eau, zones humides). PAS de mention CDPENAF ni du Décret 2016-1190 (qui sont spécifiques à l'EPA)
- **Prestations détaillées** : inventaires 4 saisons (printemps, été, automne, hiver), expertise pédologique zones humides, rédaction VNEI, dossier "Loi sur l'Eau" si applicable, dossier dérogation espèces protégées (CNPN) si applicable
- **Calendrier de prestation** sur 12-18 mois (cycle biologique complet)
- **Bon de commande signé** avec validation YouSign / signature Sylvain FREDERIC ou habilité

**Nommage observé probable** : `PTF_[BE]_ENERVIVO_[Mention]_[Commune]_[Dept]_[YYYYMMDD]_signed_.pdf`. Mentions possibles : `Enviro`, `VNEI`, `EIE`, `Faune_Flore`, `Etude_Impact`, `Loi_eau`.

**Localisation** : `7 - Achat-Fournisseurs/1-Consultations/EIE` ou `Enviro` ou par BE prestataire.

**Stratégie de classification (vs Devis EPA)** :

1. Si mention explicite **"Étude Préalable Agricole" / "CDPENAF" / "Décret 2016-1190"** → Devis EPA
2. Si mention **"Étude d'impact" / "VNEI" / "Faune Flore" / "zones humides" / "Code de l'environnement R. 122-2"** → Devis Enviro
3. **Cas mixte** : certains BE proposent les deux dans le même devis (cf. exemple Artifex avec EPA + APER + Agropédologique) → classifier selon la **prestation principale** ou flagger comme "Devis multi-prestations"
4. **Drafts ignorés** : sans signature YouSign / manuscrite → non valide pour le jalon

---

## 14. DT — DT résumé

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Document généré automatiquement par le téléservice national "reseaux-et-canalisations.gouv.fr"** (INERIS), obligatoire avant tout chantier impactant des réseaux. La DT (Déclaration de Travaux) est faite **avant le démarrage des travaux** par le maître d'ouvrage pour interroger tous les exploitants de réseaux (Enedis, mairie, opérateurs eau/gaz/télécom). On cherche **le résumé du dossier de consultation** (pas les CERFA personnalisés envoyés à chaque exploitant).

**Format observé** : PDF d'environ 10 pages, mise en page très standardisée.

**Indices internes typiques (signature très forte)** :

- **En-tête page 1** : drapeau **République Française** + logo **INERIS** + slogan **"construire sans détruire"** + bandeau "Les exploitants de tous les réseaux en 1clic"
- **Titre** : "Dossier de consultation n° [Numéro]"
- **Format du numéro de dossier** : `AAAAMMJJ00000C` (ex : `2025082500322TNL`) — la date est encodée au début (25/08/2025 → 20250825), puis numéro de séquence, puis suffixe alphanumérique
- **Encadré clé page 2** : "Nature de la consultation : **DT**" (champ explicite — c'est ICI qu'on distingue DT vs DICT)
- **Champs structurés** : "Informations sur le responsable du projet" (raison sociale ENERVIVO, adresse), "Informations sur le dossier" (localisation, INSEE, date de consultation), "Date prévue pour le commencement des travaux"
- **Plan d'emprise** (page 3) : capture cartographique du chantier en bleu
- **Coordonnées GML/géoréférencées** : EPSG:4171, RGF 93, polygones avec sommets lat/long
- **Liste des exploitants concernés** : tableau avec Enedis, mairie, SAUR, opérateurs télécom, etc.
- **Pied de page** récurrent : "Dossier n° [N°dossier] Page X / Y"

**Nommage observé** : `[N°dossier]_DT_resume.pdf` (ex : `2025082500322TNL_DT_resume.pdf`).

**Localisation** : `6 - Techniques/DICT/[N°dossier]_DDC/` (le dossier porte le n° du dossier de consultation).

**Pièges à éviter** :

1. **Ne pas confondre DT et DICT** : utiliser **uniquement le champ "Nature de la consultation"** en page 2 — c'est l'indicateur fiable. Le nom de fichier peut être trompeur si mal rangé.
2. **Ne pas confondre avec les CERFA 14434*03** personnalisés (un par exploitant, plusieurs PDFs) : on veut le **résumé global**, pas les CERFA individuels
3. **Cas DT-DICT conjointe** (suffixe `_DDC_` dans le nom) : un seul résumé couvre les deux — marquer DT ET DICT comme "Présent" et lier au même fichier

---

## 15. DICT — DICT résumé

- **Jalon** : J2a (décision Julien — habituellement plutôt Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Document généré par le **même téléservice "reseaux-et-canalisations.gouv.fr"** que la DT, mais à un stade ultérieur : la DICT (Déclaration d'Intention de Commencement de Travaux) est faite **par l'exécutant des travaux (entreprise de chantier)** juste avant le démarrage effectif des travaux (typiquement dans les 3 mois précédant). Confirme l'identification des réseaux et permet le démarrage.

**Format observé** : **strictement identique à la DT** (même téléservice, même mise en page, même structure de fichier).

**Indices internes typiques (le SEUL champ qui distingue DT et DICT)** :

- **Page 2 — encadré "Informations sur le dossier"** : "Nature de la consultation : **DICT**"
- Tout le reste de la structure est identique au document DT

**Nommage observé** : `[N°dossier]_DICT_resume.pdf`.

**Piège critique** : **ne pas se fier au nom de fichier seul** car le pattern est identique à la DT. **Toujours lire le champ "Nature de la consultation" en page 2** pour classifier de façon fiable.

**Cas DT-DICT conjointe** : si nom contient `_DDC_` (ex : `2026040800259T_DDC_resume.pdf`) = consultation conjointe — un seul résumé couvre les deux documents (DT + DICT marqués Présent + liés au même fichier).

---

## 16. Plan de masse version J2a

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2a du Plan de masse — mêmes principes que J1 (cf. doc #3), avec les indices de jalon suivants :

- **Cartouche** : `Phase : APD` (Avant-Projet Détaillé) ou maintien `APS` selon convention BE
- **Indice de révision** : typiquement `Ind B` (la lettre suit le J1 en `Ind A`)
- **Caractéristiques techniques** : données mieux renseignées que J1 (modèle de module précisé, surface projetée affinée)
- **Adaptations post-J1** : intègre les retours du CU, les contraintes urbanistiques, l'adaptation au parcellaire après géomètre

**Stratégie de classification** : si dossier contient plusieurs plans avec `Ind A` (J1) et `Ind B` (J2a) → le J2a est la version postérieure dans le temps avec des modifications listées dans le cartouche "Modification".

---

## 17. TADD version J2a

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2a du TADD — mêmes principes que J1 (cf. doc #4), avec les évolutions suivantes :

- Hypothèses de production **affinées post-PVsyst J2a**
- Données foncières confirmées (surface définitive après géomètre)
- Numéro de version interne typiquement plus élevé que TADD J1 (ex : v5 → v6 ou v6 → v6_6)
- Jalon `J2A` ou `J2a` dans le nom si convention respectée

---

## 18. Carte Nationale d'Identité (CNI) (proprio personne physique)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Copie de la Carte Nationale d'Identité du propriétaire (recto-verso). **Peut être un scan ou une photo prise au smartphone** (qualité variable, parfois floue). Identifiable par le format officiel CNI française (République Française, drapeau, photo d'identité, nom, prénoms, date de naissance, numéro CNI). Si passeport à la place → accepter comme pièce d'identité équivalente.

**Format observé** : PDF (scan) ou JPG/PNG (photo).

**Nommage probable** : `CNI_[NomProprio].pdf`, `Piece_identite_[Nom].jpg`.

**Pièges** :

- Qualité parfois faible (photo floue, pliures, mauvaise luminosité)
- Recto seul = incomplet (besoin recto-verso)
- Dates d'expiration non vérifiées par le LLM

---

## 19. Copie livret de famille (proprio personne physique)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Copie du livret de famille du propriétaire. Document officiel multi-pages avec en-tête "République Française" et mention "Livret de famille". Contient les actes de mariage, naissances des enfants, décès. Pour la PDB on s'intéresse principalement aux pages identifiant le couple et leur régime matrimonial.

**Format observé** : PDF scan, 2 à 8 pages selon composition familiale.

**Indices internes** :

- Couverture "LIVRET DE FAMILLE" + "République Française"
- Tampon de mairie sur les actes
- Mentions des actes de mariage, naissances, divorces

**Nommage probable** : `Livret_famille_[NomProprio].pdf`.

**Piège** : pages partielles fréquentes — livret incomplet si seul l'acte de mariage est scanné, sans les naissances.

---

## 20. Statuts société (proprio personne morale)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Statuts à jour de la société propriétaire (si le terrain est détenu par une SCI, EARL, GAEC, SARL, SCEA, etc.). **Doivent être à jour et signés** (pas une version draft).

**Format observé** : PDF multi-pages (15-30 pages typiquement), document juridique avec articles numérotés.

**Indices internes typiques** :

- **Titre** : "STATUTS DE LA SOCIÉTÉ [Nom]"
- **Articles** : Article 1 (Forme), Article 2 (Dénomination), Article 3 (Objet), Article 4 (Siège social), Article 5 (Capital), Article 6 (Apports), Article 7 (Gérance)…
- **Mentions clés** : capital social en euros, RCS, SIREN, adresse du siège, identité des associés
- **Pages signatures** : paraphes en bas de chaque page + signatures finales des associés
- **Dernière page** : "Fait à [ville], le [date]", signatures
- Parfois mention "Statuts mis à jour suite à AGE du [date]"

**Nommage probable** : `Statuts_[NomSociete].pdf`, `Statuts_a_jour_[Societe]_[date].pdf`.

**Pièges** :

- **Statuts non signés** = draft → non valide
- **Statuts non à jour** : si AGE postérieure les a modifiés, version obsolète
- Vérifier qu'il s'agit bien des statuts du **propriétaire foncier** (pas d'une autre société)

---

## 21. Extrait Kbis à jour (proprio personne morale)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Extrait Kbis du Registre du Commerce et des Sociétés (RCS) attestant l'existence légale et l'identité de la société propriétaire. **Doit être à jour et signé** (typiquement < 3 mois) — un Kbis ancien n'est pas valide.

**Format observé** : PDF officiel, 1 à 3 pages, généré par Infogreffe ou le greffe du tribunal de commerce.

**Indices internes typiques** :

- **En-tête** : "EXTRAIT D'IMMATRICULATION PRINCIPALE AU REGISTRE DU COMMERCE ET DES SOCIÉTÉS" ou "Extrait Kbis"
- **Mentions officielles** : "Greffe du Tribunal de Commerce de [ville]"
- **Informations** : dénomination sociale, forme juridique, capital social, SIREN/SIRET, adresse siège, gérance, date d'immatriculation, objet social, durée
- **Tampon ou signature électronique** du greffier en fin de document
- **Mention de validité** : "Extrait délivré le [date]" ou "Document à jour au [date]"
- **Logos** : Infogreffe, RCS, Greffe

**Nommage probable** : `Kbis_[Societe]_[date].pdf`, `Extrait_Kbis_[Societe].pdf`.

**Pièges à éviter** :

- **Kbis > 3 mois** = potentiellement obsolète → flag Ambigu avec note "Date Kbis à vérifier"
- **Kbis non signé / sans tampon greffier** = document non valide
- Ne pas confondre avec un avis de situation Insee (qui est différent)

---

## 22. Relevé d'identité bancaire (RIB)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Relevé d'Identité Bancaire au nom du propriétaire (personne physique ou morale), permettant le versement des redevances et loyers du bail emphytéotique.

**Format observé** : PDF ou image, 1 page typiquement.

**Indices internes typiques** :

- **En-tête banque** : logo (BNP Paribas, Crédit Agricole, Caisse d'Épargne, Banque Populaire, LCL, Société Générale, etc.)
- **Mentions obligatoires** : "Relevé d'Identité Bancaire" ou "RIB"
- **Code IBAN** : FR76 XXXX XXXX XXXX XXXX XXXX XXX (27 caractères)
- **Code BIC** : 8 ou 11 caractères
- **Nom du titulaire** : doit correspondre au nom du propriétaire de la PDB
- Code banque, code guichet, numéro de compte

**Nommage probable** : `RIB_[NomProprio].pdf`.

**Piège** : le RIB peut être au nom du conjoint ou d'une autre personne — vérifier que le nom du titulaire correspond bien au Promettant de la PDB. Si nom différent → flag Ambigu.

---

## 23. Titre de propriété des parcelles

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Acte notarié complet attestant la propriété des parcelles du projet. **Toutes les pages doivent être en PDF (pas de photos)** comme stipulé dans l'Annexe 3 de la PDB.

**Format observé** : PDF scanné ou numérique, **10 à 20+ pages**. Document juridique dense émis par un Office Notarial.

**Indices internes typiques** :

- **En-tête** : nom de l'Office Notarial, "Maître [Nom]", ville, "Notaire(s) Associé(s)"
- **Structure en 2 parties** : "PARTIE NORMALISEE" (document hypothécaire) + "PARTIE DEVELOPPEE" (clauses)
- **Sections clés** : "IDENTIFICATION DES PARTIES" (VENDEUR / ACQUEREUR), "DESIGNATION DU BIEN" avec **tableau cadastral** (Section / N° / Lieudit / Surface en ha, a, ca / Nature : pré, terre, taillis), "EFFET RELATIF" (historique de propriété, donations antérieures publiées au service de la publicité foncière), "PRIX", "CONDITIONS ET DECLARATIONS GENERALES", "ORIGINE DE PROPRIETE"
- **Mention publication** : "publié au service de la publicité foncière de [ville]", volume, numéro
- **Page de signature** : signatures manuscrites ou électroniques (tablette numérique) du vendeur et de l'acquéreur, mention "Fait à [ville], le [date]"

**Nommage observé** : `YYYY_MM_DD_[CODEPROJET]_titre_de_propriété.pdf` (ex : `2025_04_25_DLAUGA_titre_de_propriété.pdf`).

**Piège** : ne pas confondre avec l'attestation de vente du notaire (document court 1-2 pages, cf. doc #24). Le titre de propriété est **l'acte complet** (10+ pages), l'attestation est un **résumé certifié**.

---

## 24. Attestation de vente notaire (< 2 ans) ou relevé de propriété mairie

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Attestation courte rédigée et signée par le notaire, certifiant la propriété des parcelles. Document de **moins de 2 ans** (ou relevé de propriété tamponné par la mairie en alternative).

**Format observé** : PDF, **1 à 2 pages**, document notaire simple.

**Indices internes typiques** :

- **En-tête** : "OFFICE NOTARIAL", nom(s) du/des notaire(s), adresse de l'étude, logo Notaires
- **Titre** : "ATTESTATION" (en gros)
- **Formule type** : "JE SOUSSIGNE Maître [Nom], Notaire et membre de la Société Civile Professionnelle [...], CERTIFIE ET ATTESTE, QUE les biens ci-après désignés :"
- **Localisation + tableau cadastral** : "A [COMMUNE] ([CP]), Lieu-dit [nom]", tableau Section / N° / Lieudit / Surface
- **Identification des propriétaires** : noms, dates de naissance, adresses, mention usufruit/nue-propriété si applicable
- **Clôture** : "EN FOI DE QUOI, j'ai délivré la présente attestation pour servir et valoir ce que de droit", "Fait à [ville], Le [date]", nom du notaire + **signature manuscrite + cachet de l'étude notariale**
- Pied de page : "MEMBRE D'UN CENTRE DE GESTION AGREEE"

**Cas alternatif (relevé de propriété mairie)** : document tamponné, daté et signé par la mairie, contenant la liste des parcelles avec sections cadastrales.

**Nommage observé** : `YYYY_MM_DD_[CODEPROJET]_attestation_de_vente.pdf` (ex : `2025_08_25_DBOURDALE-DUFAU_attestation_de_vente.pdf`).

**Piège** : vérifier la date d'émission — doit être **de moins de 2 ans** au moment de l'audit. Si la date "Fait à [ville], Le [date]" remonte à plus de 2 ans → document périmé, flag Ambigu.

---

## 25. Copie baux en cours + coordonnées preneurs

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Copie de tous les baux ruraux en cours sur les parcelles objet de la PDB (baux à ferme, baux ruraux), avec les coordonnées des preneurs (locataires-exploitants). Permet à EnerVivo de connaître les engagements locatifs existants et d'organiser la libération des parcelles ou la coactivité.

**Format observé** : PDF, plusieurs pages (chaque bail fait 5-15 pages), peut être plusieurs fichiers si plusieurs baux.

**Indices internes typiques** :

- **Titre** : "BAIL RURAL" ou "BAIL À FERME"
- **Mention article L. 411-1 et suivants du Code rural**
- **Identification du bailleur** (propriétaire) et **preneur** (exploitant agricole)
- **Désignation des parcelles** : tableau cadastral
- **Durée du bail** : 9 ans (durée légale minimale du bail rural), renouvelable
- **Fermage** : montant annuel en €/ha
- **Signatures** : bailleur + preneur

**Nommage probable** : `Bail_rural_[Proprio]_[Preneur]_[date].pdf`, `Baux_en_cours_[CodeProjet].pdf`.

**Piège** : il peut y avoir **plusieurs baux** sur les mêmes parcelles (succession de preneurs) — chercher tous les baux actifs. Coordonnées preneurs souvent en première page du bail.

---

## 26. Relevé d'hypothèques (état hypothécaire)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Document obtenu auprès du **Service de Publicité Foncière** (ex-Conservation des Hypothèques) attestant des inscriptions hypothécaires éventuelles sur les parcelles. **Uniquement sur demande spécifique du Bénéficiaire** (EnerVivo) — pas systématique.

**Format observé** : PDF, document administratif officiel.

**Indices internes typiques** :

- **En-tête** : "Service de la publicité foncière de [ville]" ou "République Française - Ministère des Finances"
- **Titre** : "État hypothécaire" ou "Relevé d'inscriptions hypothécaires"
- **Mentions** : "Hypothèques", "Inscriptions", "Privilèges", "Saisies"
- **Identification du bien** : références cadastrales, propriétaire
- **Mention clé** : "Aucune inscription" si parcelles libres, ou détail des inscriptions si grevées
- **Tampon et signature** du conservateur des hypothèques

**Nommage probable** : `Etat_hypothecaire_[CodeProjet]_[date].pdf`, `Releve_hypotheques_[Proprio].pdf`.

**Piège** : document souvent absent si non demandé explicitement par EnerVivo (cas par cas).

---

## 27. Relevé parcellaire à jour

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

**Relevé d'exploitation émis par la MSA** (Mutualité Sociale Agricole) listant l'ensemble des parcelles exploitées par un agriculteur avec leur désignation cadastrale, surface et revenu cadastral réel. **Attention** : ce document s'appelle "Relevé d'exploitation" (pas "relevé parcellaire") dans le jargon MSA — mais c'est bien ce qui correspond à la pièce "Relevé parcellaire" de l'Annexe 3 PDB.

**Format observé** : PDF, **multi-pages** (souvent 3-8 pages selon le nombre de parcelles).

**Indices internes typiques (signature très forte)** :

- **Logo MSA** en haut à gauche : "santé / famille / retraite / services" + nom de la caisse régionale (ex : "MSA Ile de France")
- **Logo "cerfa en cours"** en haut à droite
- **Titre encadré** : "RELEVE D'EXPLOITATION"
- **Mention** : "situation cadastrale au : [date]"
- **Bloc destinataire** : nom de l'exploitant (Mme/M.), nom de l'exploitation (ex : "FRM LES AIGREFOINS"), adresse
- **Référence** : "Réf : [SIRET]" (numéro SIRET de l'exploitation)
- **Numéro de dossier** à droite : 6 chiffres (ex : "001464")
- **Tableau structuré** : DEPT / COM / NUMERO (compte propriétaire) / SECTION / NUMERO PLAN / Sub.Fisc / CLASSE / SUPERFICIE (Ha, A, Ca) / R.C REEL (Euros, Cts) / Faire Valoir (F=Fermier, D=Direct, M=Métairie) / NOM DU PROPRIETAIRE
- **Totaux par compte** : "* TOTAL DU COMPTE ="
- **Totaux par commune** et **parcellaire total** en fin de document
- **Pied de page** : "MSA [Caisse]", adresse, tél, fax, site web, "folio X/Y"

**Nommage observé** : `YYYY_MM_DD_[CODEPROJET]_Relevé_parcellaire_[Nom_Exploitant].pdf` (ex : `2026_05_13_D2JUMEAUX_Relevé_parcellaire_Anne_Huges.pdf`).

**Piège** : le nom de fichier dit "Relevé parcellaire" mais le document dit "RELEVE D'EXPLOITATION" — les deux désignent la même pièce pour l'Annexe 3 PDB. Ne pas chercher un document intitulé exactement "Relevé parcellaire" — chercher le relevé MSA.

---

## 28. Lettre de motivation projet agrivoltaïque

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Lettre rédigée par le propriétaire/exploitant agricole justifiant l'intérêt du projet agrivoltaïque pour son exploitation. **Spécifique aux projets AgriPV** (centrales sol sur parcelles agricoles). Document central pour la CDPENAF et le cadre APER (Loi 2023-175).

**Format observé** : Word/PDF, document court 1-2 pages.

**Indices internes typiques** :

- **Format** : lettre type avec en-tête (nom + adresse exploitant), destinataire (EnerVivo / Préfecture / DDT)
- **Contenu** :
  - Présentation de l'exploitation (nature, surface, productions)
  - Motivations pour le projet agrivoltaïque : maintien activité, complément revenu, amélioration bien-être animal, adaptation changement climatique, protection aléas
  - Engagement à poursuivre l'activité agricole pendant la durée du bail
  - Référence aux 4 services APER (Loi 2023-175 art. L. 314-36) si projet agrivoltaïque
- **Signature manuscrite** du propriétaire/exploitant
- **Date et lieu**

**Nommage probable** : `Lettre_motivation_[Proprio]_[CodeProjet].pdf`, `Motivation_projet_agriPV_[Nom].docx`.

**Piège** : lettre type peu personnalisée → moins crédible aux yeux de la DDT/CDPENAF. Vérifier que la lettre fait référence aux spécificités de l'exploitation.

---

## 29. Déclaration ICPE OU attestation non-assujettissement

- **Jalon** : J2a
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Deux cas possibles** selon que le projet est classé ICPE ou non :

**Cas 1 (le plus courant pour les projets AgriPV EnerVivo) : Attestation de non-classement ICPE**

**Format observé** : PDF, **1 page**, document minimaliste.

**Indices internes typiques** :

- **En-tête** : raison sociale du propriétaire/gérant du site (ex : "SCI ABEZIE")
- **Titre** : "ATTESTATION" (en gros, centré)
- **Corps** : formule type "Je soussigné [Nom], gérant de [Société], déclare sur l'honneur que le site immobilier sis [adresse complète], **n'est pas classé en Installations Classées pour la Protection de l'Environnement (ICPE)**."
- **Clôture** : "Fait pour valoir ce que de droit.", lieu, date
- **Signature manuscrite** du déclarant
- **Pied de page** (optionnel) : adresse complète + numéro RCS

**Nommage observé** : `Attestation_non_classement_ICPE.pdf`, `ICPE_attestation_non_assujettissement_[Commune].pdf`.

**Cas 2 : Déclaration ICPE (si assujetti)**

Document administratif de type récépissé préfectoral de déclaration ICPE. En-tête préfecture, numéro de dossier, rubriques ICPE concernées. Beaucoup plus long (5-20 pages). Cas rare pour les projets sol < 250 kWc mais possible pour les grands parcs.

**Stratégie de classification** : si le document fait 1 page avec "déclare sur l'honneur" + "non classé ICPE" → attestation non-classement. Si document officiel préfectoral avec rubriques ICPE → déclaration ICPE.

---

## 30. RIB pour versement redevances et loyers du bail

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

**Doublon potentiel avec doc #22** (RIB) — peut être le même document. Si distinct : RIB spécifiquement dédié aux versements des redevances du bail emphytéotique (souvent un compte dédié pour les revenus locatifs).

**Stratégie** : si un seul RIB trouvé pour le propriétaire, il couvre les deux exigences (doc #22 et #30). Si deux RIB distincts → typiquement un compte principal + un compte dédié aux revenus fonciers.

Indices et format identiques au doc #22.

---

## 31. Attestation MSA chef d'exploitation (< 6 mois)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Attestation officielle émise par la **MSA** (Mutualité Sociale Agricole) confirmant le statut de **chef d'exploitation agricole** du propriétaire/exploitant. **Contrainte de fraîcheur stricte : moins de 6 mois** au moment de l'audit.

**Format observé** : PDF, 1 à 2 pages, document officiel MSA.

**Indices internes typiques** :

- **En-tête MSA** : logo "santé / famille / retraite / services" + nom de la caisse régionale
- **Titre** : "Attestation" ou "Attestation de chef d'exploitation"
- **Mention clé** : "chef d'exploitation agricole", "à titre principal" ou "à titre secondaire"
- **Identification** : nom, prénom, date de naissance, SIRET de l'exploitation, surface exploitée
- **Date d'émission** : doit être < 6 mois
- **Signature ou tampon MSA**

**Nommage probable** : `Attestation_MSA_[Proprio]_[date].pdf`, `MSA_chef_exploitation_[Nom].pdf`.

**Piège clé** : **vérifier la date d'émission** — si > 6 mois, le document est périmé et doit être renouvelé → flag Ambigu avec note "Date attestation MSA > 6 mois, à renouveler". C'est un piège fréquent.

---

## 32. Dossier de qualification J2a

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2a du Dossier de qualification — mêmes principes que J1 (cf. doc #5), avec contenu plus étoffé :

- **Jalon `J2a` explicite dans le nom** du fichier
- Intègre le CU obtenu, les devis EPA/Enviro lancés, le plan de masse APD, le TADD affiné J2a
- Slides supplémentaires sur les contraintes urbanistiques (PLUi, SCoT, servitudes)
- Slides sur la concertation locale (synthèses des CR mairie, EPCI, Chambre d'Agriculture)

**Stratégie de classification** : identique à doc #5, jalon explicite dans nom de fichier (`_J2a_` ou `_J2A_`).

---

## 33. Lettre d'engagement

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Lettre d'engagement signée par EnerVivo (ou par le propriétaire selon contexte) formalisant un engagement ponctuel : engagement à respecter certaines prescriptions, à mettre en œuvre des mesures de compensation, à maintenir certains usages, etc.

**Format observé probable** : Word/PDF, lettre type 1-2 pages signée.

**Indices internes** :

- **Format lettre** : en-tête EnerVivo (logo + adresse Bordeaux), destinataire identifié
- **Titre** : "Lettre d'engagement" ou "Engagement de [thème spécifique]"
- **Corps** : objet de l'engagement, conditions, durée
- **Signature** : Sylvain FREDERIC ou habilité EnerVivo

**Nommage probable** : `Lettre_engagement_[Theme]_[CodeProjet].pdf`.

**Piège** : document non standardisé, contenu très variable selon contexte. À traiter comme document opportuniste — si présent c'est un plus mais pas bloquant.
