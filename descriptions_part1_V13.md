# Descriptions enrichies — Référentiel documents par jalon VivEpic

**Version** : V13
**Source** : référentiel V12 + modifications Julien (fusion DT/DICT, CR RDV formats, EPA, onduleurs, lettre motivation)
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

## ⚠️ Modifications V13 — Résumé des changements

1. **Fusion DT/DICT** : les anciens docs #14 (DT) et #15 (DICT) sont fusionnés en un seul doc #14 "DT / DICT - résumé". Tous les documents à partir de l'ancien #16 ont été renumérotés (ancien #16 → nouveau #15, etc.). Total V13 : **106 documents**.
2. **CR RDV (#7, 8, 9, 10, 32)** : formats acceptés clarifiés — feuilles d'émargement, mails, notes, prises de notes, CR formels.
3. **EPA (#12, #36)** : distinction renforcée — étude technico-économique agricole, pas étude environnementale.
4. **Lettre de motivation (#26)** : lettre de l'agriculteur/exploitant, pas d'EnerVivo.
5. **Tests onduleurs (#100)** : tests fonctionnels de mise en route, pas tests harmoniques.

---

# AVANT J1 — Qualification

## 1. LOI signée

- **Jalon** : Avant J1
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

Lettre d'Intention signée par le propriétaire foncier et VivEpic/EnerVivo, formalisant l'accord de principe pour étudier le projet photovoltaïque sur ses parcelles. Document précédant la PDB.

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
- **Cartouche dossier** : `DOSSIER N° CU [code INSEE] [Année] [N°]` (ex : `CU 47175 25 B0109`)
- **Article 2 clé** : "Le terrain objet de la demande peut être utilisé pour la réalisation de l'opération envisagée" (= validation)
- **Signature** : "Fait à [commune], le [date]", "Par délégation, Le Maire Adjoint, [Nom]" avec cachet de mairie

**Nommage observé** : `CU_[INSEE]_[AA]_B[N°]-arrete_decision_[X]_[Y].pdf` (ex : `CU_47175_25_B0109-arrete_decision_1_1.pdf`).

**Pièges à éviter** :
1. **Ne pas confondre avec un CU d'information (type a)** — chercher absolument "OPERATIONNEL" dans le titre
2. **Ne pas confondre avec la demande de CU** (CERFA 13410, formulaire vide) — on veut **l'arrêté de décision**
3. **Vérifier la validité** : un CU est valable 18 mois — si daté de plus de 18 mois et pas prorogé, il est caduc

---

## 7. Compte-rendu RDV maire et élus

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple — 1 par RDV)

### Description

Trace écrite des échanges lors d'un RDV avec le maire, l'équipe municipale ou des élus locaux (conseillers, adjoints). Document préparatoire pour démontrer la concertation locale. **Peut être multiple : 1 par RDV** (souvent plusieurs RDV avant validation J2a).

**🚨 Formats acceptés (tous valides)** :
- **Compte-rendu formel** : document Word ou PDF structuré avec en-tête EnerVivo, liste des participants, points abordés, décisions, actions à mener
- **Mail reçu ou échangé** : email de la mairie, du maire, d'un élu ou d'EnerVivo relatant un échange ou donnant suite à une réunion (format `.msg`, `.eml`, ou PDF d'un mail imprimé)
- **Notes prises lors du RDV** : fichier texte `.txt`, fichier Word `.docx`, notes manuscrites scannées — même informel, si la date et l'interlocuteur sont identifiables
- **Feuille d'émargement** : tableau signé des participants (peut accompagner un CR ou exister seul comme preuve de réunion)
- **Prise de notes partagée** : document partagé (OneNote, Google Docs exporté, etc.) contenant les notes de réunion

**Indices discriminants (interlocuteur = mairie)** :
- Participants mentionnent : "Maire de [commune]", "Monsieur/Madame le Maire", "Adjoint au maire", "Conseiller municipal", "Mairie de [Commune]"
- Objet ou sujet : présentation du projet, avis de la commune, soutien politique, retombées fiscales (IFER, taxes foncières)

**Nommage probable** : `CR_RDV_Mairie_[Commune]_[date].docx`, `Compte-rendu_Mairie_[Commune]_YYYYMMDD.pdf`, `Note_RDV_Mairie_[date].txt`.

**Localisation** : `4 - Documents Administratifs/Comptes-rendus` ou `Comptes-rendus mairie`.

**Stratégie de classification** :
1. Distinguer du CR EPCI, Chambre d'Agriculture, DDT, SDIS → utiliser **les participants ou l'objet** pour discriminer
2. **Plusieurs CR par projet attendus** : ne pas filtrer sur l'unicité, lister tous les CR avec dates
3. Si format peu structuré (notes manuscrites scannées, mail informel) : acceptable → ne pas rejeter pour cause de format

---

## 8. Compte-rendu RDV EPCI / ComCom

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple)

### Description

Trace écrite de réunion avec l'Établissement Public de Coopération Intercommunale (communauté de communes ou communauté d'agglomération). Même nature que le CR mairie mais avec un interlocuteur intercommunal. Concerne typiquement le schéma de cohérence territorial (SCoT), les enjeux paysagers à échelle intercommunale, ou la position politique de l'EPCI sur l'ENR.

**🚨 Formats acceptés** : identiques au doc #7 — compte-rendu formel, mail, notes, feuille d'émargement, prise de notes. Voir doc #7 pour le détail.

**Discriminant** : les participants mentionnent un président de ComCom, DGS intercommunal, élu EPCI, ou mention explicite "Communauté de communes de [nom]" / "EPCI" / "ComCom" dans l'objet ou les participants.

**Nommage probable** : `CR_RDV_EPCI_[Commune]_[date]`, `CR_ComCom_[nom]_[date]`.

**Piège** : ne pas confondre avec le CR mairie. Discriminer sur l'interlocuteur (mairie = commune seule, EPCI = échelon intercommunal).

---

## 9. Compte-rendu RDV Chambre d'Agriculture

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple)

### Description

Trace écrite de réunion avec la Chambre d'Agriculture départementale. Concerne typiquement la compatibilité du projet avec l'activité agricole locale, l'avis de la Chambre sur la compensation agricole, la position sur l'agrivoltaïsme.

**🚨 Formats acceptés** : identiques au doc #7 — compte-rendu formel, mail, notes, feuille d'émargement, prise de notes. Voir doc #7 pour le détail.

**Discriminant** : participants mentionnent un représentant de la Chambre d'Agriculture, ou mention explicite "Chambre d'Agriculture [département]" dans l'objet ou les participants.

**Nommage probable** : `CR_RDV_CA_[Dept]_[date]`, `CR_Chambre_Agriculture_[date]`.

**Piège** : ne pas confondre avec le rapport EPA final (qui intègre une analyse de la Chambre d'Agriculture mais n'est pas un CR de RDV).

---

## 10. Compte-rendu RDV DDT(M)

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique (peut être multiple)

### Description

Trace écrite de réunion avec la Direction Départementale des Territoires (et de la Mer) — administration qui instruit les autorisations d'urbanisme, les dossiers ICPE, les questions agricoles et environnementales. RDV souvent demandé par EnerVivo pour **pré-cadrer l'instruction** : comprendre la doctrine locale sur l'agrivoltaïsme, les attendus de la CDPENAF, les points de vigilance.

**🚨 Formats acceptés** : identiques au doc #7 — compte-rendu formel, mail, notes, feuille d'émargement, prise de notes. Voir doc #7 pour le détail.

**Discriminant** : participants mentionnent "DDT", "DDTM", "chef de service urbanisme", "pôle ENR de la DDT". Contenu typique : doctrine locale, seuils compensation, dossier type attendu.

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

**Piège** : ne pas confondre avec un CR de réunion (le CR a du contenu rédactionnel, la feuille d'émargement est juste un tableau de signatures). Les deux peuvent coexister pour le même comité.

---

## 12. Devis signé EPA

- **Jalon** : J2a
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

**Devis / Proposition Technique et Financière (PTF)** signé par EnerVivo auprès d'un bureau d'études pour commander l'**EPA (Étude Préalable Agricole)**. **L'étude elle-même n'est pas attendue en J2a** — c'est uniquement la commande qui valide le jalon.

**🚨 Qu'est-ce que l'EPA ?** L'EPA est une **étude technico-économique** qui analyse l'impact du projet photovoltaïque sur l'**économie agricole locale** (emplois, productions, filières, foncier agricole). Elle n'est PAS une étude environnementale (pas de faune, flore, zones humides — cela relève du devis Enviro #13). Elle répond aux exigences de la **Loi LAAAF du 13 octobre 2014** et du **Décret n° 2016-1190 du 31 août 2016** sur la compensation agricole collective. Obligatoire si emprise > 5 ha en zone agricole.

**Discrimination EPA vs Enviro** :
- **EPA** → termes clés : "Étude Préalable Agricole", "EPA", "CDPENAF", "Décret 2016-1190", "compensation agricole collective", "économie agricole", "article L. 112-1-3 Code rural"
- **Enviro** → termes clés : "VNEI", "EIE", "étude d'impact", "faune", "flore", "zones humides", "Code de l'environnement R. 122-2", "espèces protégées L. 411-1"
- **Cas mixte** : certains BE combinent EPA + études agropédologiques dans le même devis → classifier selon la **prestation principale**

**Format observé** : PDF d'environ 20-30 pages, livré par le BE prestataire (Artifex / Socotec Aménagement Biodiversité, Naldéo, Agroconsult, etc.).

**Indices internes typiques** :
- **Page de garde** : logo BE prestataire + logo EnerVivo + titre **"Etude Préalable Agricole — Proposition technique et financière"** + référence projet + commune + département + date
- **Mention "ENERVIVO" en client**, adresse 185 Boulevard Maréchal Leclerc 33000 Bordeaux
- **Cadre réglementaire** : mention **Décret n° 2016-1190**, article L. 112-1-3 du Code rural, **CDPENAF**
- **Partie "Proposition financière"** : montant HT/TTC prestations EPA
- **Bon de commande signé** : cases validation cochées + tampon **"Certifié par YouSign"** + signature Sylvain FREDERIC ou habilité EnerVivo

**Nommage observé** : `PTF_[BE]_ENERVIVO_EPA_[Mentions]_[Commune]_[Dept]_[YYYYMMDD]_signed_.pdf` (ex : `PTF_ARTIFEX_ENERVIVO_EPA_APER_Agropedo_AgriPV_Uzein_64_20251119__signed_.pdf`). Le suffixe **`_signed_`** dans le nom est un indicateur fort de signature YouSign.

**Pièges à éviter** :
1. **Drafts non signés à ignorer** : si absence du tampon YouSign ET pas de signature manuscrite → non valide
2. **Ne pas confondre avec le rapport EPA final** (livrable de l'étude attendu en J2b, 100-200+ pages)
3. **Ne pas confondre avec le devis Enviro** : l'EPA mentionne CDPENAF et Décret 2016-1190, l'Enviro mentionne Code de l'environnement et espèces protégées
4. **Cas par cas** : obligatoire uniquement si emprise > seuil départemental (défaut 5 ha)

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
- **PEDO-ZH** : étude pédologique et zones humides
- **Faune et Flore** : inventaires naturalistes (4 saisons typiquement)

**Format observé** : PDF, structure très similaire au devis EPA (mêmes BE possibles ou BE différents : Biotope, Calidris, Naldéo, Egis Environnement, etc.).

**Indices internes typiques** :
- **Page de garde** : logo BE environnemental + EnerVivo client + titre **"Proposition technique et financière — Étude d'impact"** ou **"VNEI"** ou **"Inventaires faune-flore et zones humides"**
- **Cadre réglementaire** : mention **Code de l'environnement**, articles **R. 122-2** (étude d'impact), **L. 411-1** (espèces protégées), **L. 211-1** (zones humides). **PAS de mention CDPENAF ni du Décret 2016-1190**
- **Calendrier de prestation** sur 12-18 mois (cycle biologique complet)
- **Bon de commande signé** avec validation YouSign / signature Sylvain FREDERIC

**Nommage observé probable** : `PTF_[BE]_ENERVIVO_[Mention]_[Commune]_[Dept]_[YYYYMMDD]_signed_.pdf`. Mentions possibles : `Enviro`, `VNEI`, `EIE`, `Faune_Flore`, `Etude_Impact`, `Loi_eau`.

---

## 14. DT / DICT — résumé

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**[V13 - Fusion DT + DICT]** Document généré automatiquement par le téléservice national **"reseaux-et-canalisations.gouv.fr"** (INERIS), obligatoire avant tout chantier impactant des réseaux. On cherche le **résumé du dossier de consultation** — que ce soit un résumé DT (Déclaration de Travaux), un résumé DICT (Déclaration d'Intention de Commencement de Travaux), ou un résumé conjoint DT+DICT (DDC).

**Distinction DT / DICT / DDC** :
- **DT** (Déclaration de Travaux) : faite **avant le démarrage des travaux** par le maître d'ouvrage (EnerVivo) pour interroger les exploitants de réseaux. Champ "Nature de la consultation : **DT**"
- **DICT** (Déclaration d'Intention de Commencement de Travaux) : faite **par l'exécutant des travaux (entreprise de chantier)** juste avant le démarrage effectif. Champ "Nature de la consultation : **DICT**"
- **DDC** (DT-DICT Conjoint) : consultation conjointe couvrant les deux — un seul résumé, nom contient `_DDC_` (ex : `2026040800259T_DDC_resume.pdf`) → marquer DT **ET** DICT comme "Présent", lier au même fichier

**Format observé** : PDF d'environ 10 pages, mise en page très standardisée identique pour DT, DICT et DDC.

**Indices internes typiques (communs aux trois)** :
- **En-tête page 1** : drapeau **République Française** + logo **INERIS** + slogan **"construire sans détruire"**
- **Titre** : "Dossier de consultation n° [Numéro]"
- **Format du numéro de dossier** : `AAAAMMJJ00000C` (ex : `2025082500322TNL`)
- **Encadré clé page 2** : "Nature de la consultation : **DT**" / "**DICT**" / "**DT-DICT**" — c'est ICI que se fait la discrimination
- **Champs structurés** : "Informations sur le responsable du projet" (raison sociale ENERVIVO, adresse), coordonnées GML/géoréférencées, liste des exploitants concernés

**Nommage observé** :
- DT : `[N°dossier]_DT_resume.pdf` (ex : `2025082500322TNL_DT_resume.pdf`)
- DICT : `[N°dossier]_DICT_resume.pdf`
- DDC : `[N°dossier]_DDC_resume.pdf`

**Localisation** : `6 - Techniques/DICT/[N°dossier]_DDC/`

**Stratégie de classification** :
1. **Ne jamais se fier au nom de fichier seul** — toujours lire le champ **"Nature de la consultation"** en page 2
2. Si `Nature : DT` → DT validé ✓ / DICT à chercher séparément (peut être absent si pas encore lancé)
3. Si `Nature : DICT` → DICT validé ✓ / DT à chercher séparément (peut être dans un autre fichier)
4. Si `Nature : DT-DICT` ou nom contient `_DDC_` → DT **ET** DICT tous deux validés ✓ (un seul fichier suffit)

**Pièges à éviter** :
1. **Ne pas confondre DT et DICT** : le champ "Nature de la consultation" en page 2 est **l'unique indicateur fiable**
2. **Ne pas confondre avec les CERFA 14434*03** personnalisés (un par exploitant) : on veut le **résumé global**
3. **Un projet peut avoir les deux séparément** : DT (lancé avant J2a) + DICT (lancé avant démarrage chantier en J5) → deux fichiers distincts, tous deux attendus

---

## 15. Plan de masse version J2a

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

## 16. TADD version J2a

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

## 17. Carte Nationale d'Identité (CNI) (proprio personne physique)

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

## 18. Copie livret de famille (proprio personne physique)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Copie du livret de famille du propriétaire. Document officiel multi-pages avec en-tête "République Française" et mention "Livret de famille". Contient les actes de mariage, naissances des enfants, décès.

**Format observé** : PDF scan, 2 à 8 pages selon composition familiale.

**Indices internes** :
- Couverture "LIVRET DE FAMILLE" + "République Française"
- Tampon de mairie sur les actes
- Mentions des actes de mariage, naissances, divorces

**Nommage probable** : `Livret_famille_[NomProprio].pdf`.

---

## 19. Statuts société (proprio personne morale)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Statuts à jour de la société propriétaire (si le terrain est détenu par une SCI, EARL, GAEC, SARL, SCEA, etc.). **Doivent être à jour et signés** (pas une version draft).

**Format observé** : PDF multi-pages (15-30 pages typiquement), document juridique avec articles numérotés.

**Indices internes typiques** :
- **Titre** : "STATUTS DE LA SOCIÉTÉ [Nom]"
- **Articles** : Article 1 (Forme), Article 2 (Dénomination), Article 3 (Objet), Article 4 (Siège social), Article 5 (Capital)…
- **Pages signatures** : paraphes en bas de chaque page + signatures finales des associés
- Parfois mention "Statuts mis à jour suite à AGE du [date]"

**Nommage probable** : `Statuts_[NomSociete].pdf`, `Statuts_a_jour_[Societe]_[date].pdf`.

**Pièges** :
- **Statuts non signés** = draft → non valide
- **Statuts non à jour** : si AGE postérieure les a modifiés, version obsolète
- Vérifier qu'il s'agit bien des statuts du **propriétaire foncier** (pas d'une autre société)

---

## 20. Extrait Kbis à jour (proprio personne morale)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Extrait Kbis du Registre du Commerce et des Sociétés attestant l'existence légale et l'identité de la société propriétaire. **Doit être à jour** (typiquement < 3 mois).

**Format observé** : PDF officiel, 1 à 3 pages, généré par Infogreffe ou le greffe du tribunal de commerce.

**Indices internes typiques** :
- **En-tête** : "EXTRAIT D'IMMATRICULATION PRINCIPALE AU REGISTRE DU COMMERCE ET DES SOCIÉTÉS" ou "Extrait Kbis"
- **Mentions officielles** : "Greffe du Tribunal de Commerce de [ville]", SIREN/SIRET, capital social
- **Tampon ou signature électronique** du greffier en fin de document

**Pièges** :
- **Kbis > 3 mois** = potentiellement obsolète → flag Ambigu avec note "Date Kbis à vérifier"
- Ne pas confondre avec un avis de situation Insee

---

## 21. Titre de propriété des parcelles

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Acte notarié complet attestant la propriété des parcelles du projet. **Toutes les pages doivent être en PDF (pas de photos)** comme stipulé dans l'Annexe 3 de la PDB.

**Format observé** : PDF scanné ou numérique, **10 à 20+ pages**. Document juridique dense émis par un Office Notarial.

**Indices internes typiques** :
- **En-tête** : nom de l'Office Notarial, "Maître [Nom]", ville, "Notaire(s) Associé(s)"
- **Structure en 2 parties** : "PARTIE NORMALISEE" + "PARTIE DEVELOPPEE"
- **Tableau cadastral** : Section / N° / Lieudit / Surface en ha, a, ca / Nature
- **Page de signature** : signatures manuscrites ou électroniques

**Nommage observé** : `YYYY_MM_DD_[CODEPROJET]_titre_de_propriété.pdf`.

**Piège** : ne pas confondre avec l'attestation de vente du notaire (doc #22 — document court 1-2 pages).

---

## 22. Attestation de vente notaire (< 2 ans) ou relevé de propriété mairie

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Attestation courte rédigée et signée par le notaire, certifiant la propriété des parcelles. Document de **moins de 2 ans** (ou relevé de propriété tamponné par la mairie en alternative).

**Format observé** : PDF, **1 à 2 pages**, document notaire simple.

**Indices internes typiques** :
- **Titre** : "ATTESTATION" (en gros)
- **Formule type** : "JE SOUSSIGNE Maître [Nom], Notaire [...], CERTIFIE ET ATTESTE, QUE les biens ci-après désignés :"
- **Tableau cadastral** : Section / N° / Lieudit / Surface
- **Signature manuscrite + cachet de l'étude notariale**
- Pied de page : "MEMBRE D'UN CENTRE DE GESTION AGREEE"

**Nommage observé** : `YYYY_MM_DD_[CODEPROJET]_attestation_de_vente.pdf`.

**Piège** : vérifier la date d'émission — doit être **de moins de 2 ans**. Si > 2 ans → flag Ambigu.

---

## 23. Copie baux en cours + coordonnées preneurs

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Copie de tous les baux ruraux en cours sur les parcelles objet de la PDB, avec les coordonnées des preneurs (locataires-exploitants).

**Format observé** : PDF, plusieurs pages (chaque bail fait 5-15 pages), peut être plusieurs fichiers si plusieurs baux.

**Indices internes typiques** :
- **Titre** : "BAIL RURAL" ou "BAIL À FERME"
- **Mention article L. 411-1 et suivants du Code rural**
- **Identification du bailleur** (propriétaire) et **preneur** (exploitant agricole)
- **Durée du bail** : 9 ans (durée légale minimale), renouvelable

**Piège** : il peut y avoir **plusieurs baux** sur les mêmes parcelles — chercher tous les baux actifs.

---

## 24. Relevé d'hypothèques (état hypothécaire)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Document obtenu auprès du **Service de Publicité Foncière** attestant des inscriptions hypothécaires éventuelles sur les parcelles.

**Format observé** : PDF, document administratif officiel.

**Indices internes typiques** :
- **En-tête** : "Service de la publicité foncière de [ville]" ou "République Française - Ministère des Finances"
- **Titre** : "État hypothécaire" ou "Relevé d'inscriptions hypothécaires"
- **Mention clé** : "Aucune inscription" si parcelles libres, ou détail des inscriptions si grevées
- **Tampon et signature** du conservateur des hypothèques

**Piège** : document souvent absent si non demandé explicitement par EnerVivo (cas par cas).

---

## 25. Relevé parcellaire à jour

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

**Relevé d'exploitation émis par la MSA** (Mutualité Sociale Agricole) listant l'ensemble des parcelles exploitées par un agriculteur. **Attention** : ce document s'appelle "Relevé d'exploitation" dans le jargon MSA — mais c'est bien ce qui correspond à la pièce "Relevé parcellaire" de l'Annexe 3 PDB.

**Format observé** : PDF, multi-pages (souvent 3-8 pages).

**Indices internes typiques (signature très forte)** :
- **Logo MSA** en haut à gauche + nom de la caisse régionale
- **Titre encadré** : "RELEVE D'EXPLOITATION"
- **Tableau structuré** : DEPT / COM / SECTION / NUMERO PLAN / SUPERFICIE (Ha, A, Ca) / R.C REEL / Faire Valoir / NOM DU PROPRIETAIRE
- **Référence** : "Réf : [SIRET]" (numéro SIRET de l'exploitation)

**Nommage observé** : `YYYY_MM_DD_[CODEPROJET]_Relevé_parcellaire_[Nom_Exploitant].pdf`.

**Piège** : le nom de fichier dit "Relevé parcellaire" mais le document dit "RELEVE D'EXPLOITATION" — les deux désignent la même pièce. Ne pas chercher un document intitulé exactement "Relevé parcellaire".

---

## 26. Lettre de motivation projet agrivoltaïque

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

**[V13 - Précision] Lettre rédigée et signée par l'agriculteur / exploitant agricole** (le propriétaire foncier et/ou l'exploitant des parcelles) justifiant sa motivation personnelle pour le projet photovoltaïque et agricole. **Ce n'est PAS une lettre d'EnerVivo** — c'est une lettre du client (l'agriculteur ou le propriétaire-exploitant) qui exprime son adhésion au projet et décrit son intérêt agricole.

**Format observé** : **PDF ou Word signé**, document court **1 à 2 pages**, format lettre classique. La signature doit être celle de l'agriculteur/exploitant ou du propriétaire, et non d'un représentant d'EnerVivo.

**Indices internes typiques** :
- **Format lettre** : en-tête avec nom et adresse de l'agriculteur/exploitant (PAS le logo EnerVivo), date, destinataire (EnerVivo, Préfecture ou DDT selon contexte)
- **Signataire** : nom + signature manuscrite de l'agriculteur, de l'exploitant, du gérant de la structure agricole (EARL, GAEC, SCEA, etc.)
- **Contenu** :
  - Présentation de l'exploitation : nature de l'activité agricole (élevage, grandes cultures, maraîchage…), surface exploitée, productions
  - Motivations **personnelles** de l'agriculteur pour le projet agrivoltaïque : maintien et viabilité de l'exploitation, complément de revenus, amélioration du bien-être animal, adaptation au changement climatique, protection des cultures ou du bétail contre les aléas climatiques, investissement dans des pratiques durables
  - Engagement à poursuivre l'activité agricole pendant la durée du bail emphytéotique
  - Mention du projet spécifique et des parcelles concernées
  - Référence aux services rendus par l'agrivoltaïsme (Loi APER 2023-175, article L. 314-36 du Code de l'énergie) si le projet est agrivoltaïque

**Nommage probable** : `Lettre_motivation_[Proprio_ou_Exploitant]_[CodeProjet].pdf`, `Motivation_agriPV_[Nom].docx`, `Lettre_engagement_agriculteur_[CodeProjet].pdf`.

**Piège** :
- **Signataire = EnerVivo** → ce n'est PAS la lettre de motivation attendue (lettre d'EnerVivo = autre document)
- Lettre type peu personnalisée (copier-coller sans mention de l'exploitation réelle) → moins crédible aux yeux de la DDT/CDPENAF mais documentairement valide pour l'audit
- Vérifier que la lettre décrit l'**exploitation de l'agriculteur**, pas les intérêts commerciaux d'EnerVivo

---

## 27. Déclaration ICPE OU attestation non-assujettissement

- **Jalon** : J2a
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Deux cas possibles** selon que le projet est classé ICPE ou non :

**Cas 1 (le plus courant pour les projets AgriPV EnerVivo) : Attestation de non-classement ICPE**

**Format observé** : PDF, **1 page**, document minimaliste.

**Indices internes typiques** :
- **Titre** : "ATTESTATION" (en gros, centré)
- **Corps** : formule type "Je soussigné [Nom], gérant de [Société], déclare sur l'honneur que le site immobilier sis [adresse], **n'est pas classé en Installations Classées pour la Protection de l'Environnement (ICPE)**."
- **Signature manuscrite** du déclarant

**Nommage observé** : `Attestation_non_classement_ICPE.pdf`, `ICPE_attestation_non_assujettissement_[Commune].pdf`.

**Cas 2 : Déclaration ICPE (si assujetti)** : document administratif avec récépissé préfectoral. Beaucoup plus long (5-20 pages).

---

## 28. Relevé d'identité bancaire (RIB) pour versement redevances et loyers du bail

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Relevé d'Identité Bancaire au nom du propriétaire (personne physique ou morale), permettant le versement des redevances et loyers du bail emphytéotique.

**Format observé** : PDF ou image, 1 page typiquement.

**Indices internes typiques** :
- **Mentions obligatoires** : "Relevé d'Identité Bancaire" ou "RIB"
- **Code IBAN** : FR76 XXXX XXXX XXXX XXXX XXXX XXX (27 caractères)
- **Nom du titulaire** : doit correspondre au nom du propriétaire de la PDB

**Piège** : le RIB peut être au nom du conjoint ou d'une autre personne — vérifier que le nom du titulaire correspond bien au Promettant de la PDB.

---

## 29. Attestation MSA chef d'exploitation (< 6 mois)

- **Jalon** : J2a
- **Propriété** : Annexes 3 PDB
- **Versioning** : Document unique

### Description

Attestation officielle émise par la **MSA** (Mutualité Sociale Agricole) confirmant le statut de **chef d'exploitation agricole**. **Contrainte de fraîcheur stricte : moins de 6 mois** au moment de l'audit.

**Format observé** : PDF, 1 à 2 pages, document officiel MSA.

**Indices internes typiques** :
- **En-tête MSA** : logo "santé / famille / retraite / services" + nom de la caisse régionale
- **Titre** : "Attestation" ou "Attestation de chef d'exploitation"
- **Mention clé** : "chef d'exploitation agricole", "à titre principal" ou "à titre secondaire"
- **Date d'émission** : doit être < 6 mois

**Piège clé** : **vérifier la date d'émission** — si > 6 mois, le document est périmé → flag Ambigu avec note "Date attestation MSA > 6 mois, à renouveler".

---

## 30. Dossier de qualification J2a

- **Jalon** : J2a
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2a du Dossier de qualification — mêmes principes que J1 (cf. doc #5), avec contenu plus étoffé :
- **Jalon `J2a` explicite dans le nom** du fichier
- Intègre le CU obtenu, les devis EPA/Enviro lancés, le plan de masse APD, le TADD affiné J2a
- Slides sur les contraintes urbanistiques (PLUi, SCoT, servitudes) et la concertation locale (synthèses des CR mairie, EPCI, Chambre d'Agriculture)

---

## 31. Lettre d'engagement

- **Jalon** : J2a
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Lettre d'engagement signée par EnerVivo (ou par le propriétaire selon contexte) formalisant un engagement ponctuel : engagement à respecter certaines prescriptions, à mettre en œuvre des mesures de compensation, à maintenir certains usages, etc.

**Format observé probable** : Word/PDF, lettre type 1-2 pages signée.

**Indices internes** :
- **Format lettre** : en-tête EnerVivo (logo + adresse Bordeaux), destinataire identifié
- **Titre** : "Lettre d'engagement" ou "Engagement de [thème spécifique]"
- **Signature** : Sylvain FREDERIC ou habilité EnerVivo

**Piège** : document non standardisé, contenu très variable selon contexte. Si présent c'est un plus mais pas bloquant.
