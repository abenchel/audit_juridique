# Descriptions enrichies — Référentiel documents par jalon VivEpic (suite)

**Version** : V13 — partie 2 (docs #32 à #106)
**Suite de** : descriptions_part1_V13.md

---

# J2b — Permitting phase B

## 32. Compte-rendu RDV SDIS

- **Jalon** : J2b
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Trace écrite d'un échange avec le **Service Départemental d'Incendie et de Secours** (SDIS / pompiers) — autorité consultative sur les questions de sécurité incendie pour les centrales PV (accès engins de secours, défense extérieure contre l'incendie / DECI, citerne SDIS de 120m³ visible dans le plan de masse, agencement portails). RDV nécessaire pour les projets sol importants.

**🚨 Formats acceptés (identiques aux CR RDV J2a, cf. docs #7-10)** :
- **Compte-rendu formel** : document Word ou PDF structuré avec participants, points abordés, prescriptions SDIS, actions à mener
- **Mail reçu** : email du SDIS ou d'un représentant EnerVivo suite à un échange avec le SDIS
- **Notes de réunion** : fichier texte, Word, ou notes manuscrites scannées
- **Feuille d'émargement** : tableau signé des participants (accompagne souvent un CR SDIS)

**Indices discriminants (interlocuteur = SDIS)** :
- Participants mentionnent : "Capitaine", "Lieutenant", "SDIS [département]", "Service Prévention", "Colonel", "responsable prévention incendie"
- Sujets typiques : défense extérieure contre l'incendie (DECI), citerne 120m³, accès engins de secours, portails, signalétique, plans à fournir pour le PC

**Nommage probable** : `CR_RDV_SDIS_[Dept]_[date]`, `CR_SDIS_[Commune]_[date]`, `Note_SDIS_[date].pdf`.

**Piège** : ne pas confondre avec l'avis SDIS officiel sur le PC (document administratif, pas un CR interne).

---

## 33. Avis de cadrage DDTM sur projet ENR

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Avis officiel rendu par la DDT(M)** suite à une demande de cadrage préalable d'EnerVivo sur le projet ENR. Document de pré-instruction administrative qui détaille les attentes de la DDT sur le dossier PC à venir.

**Format observé** : PDF officiel administratif, 3-10 pages.

**Indices internes typiques** :
- **En-tête** : drapeau République Française + logo "Direction Départementale des Territoires de [Dept]"
- **Sections** : Contexte, Doctrine locale ENR, Compatibilité PLUi/SCoT, Points d'attention CDPENAF, Études complémentaires demandées, Cadre APER
- **Signature** : Directeur DDT ou chef de service ENR
- **Mention** : "Avis de cadrage / pré-instruction" — n'engage pas formellement la DDT mais oriente le dossier

**Nommage probable** : `Avis_cadrage_DDT[M]_[Dept]_[CodeProjet]_[date].pdf`.

**Piège** : ne pas confondre avec l'avis final sur le PC (qui vient après dépôt). Le cadrage est en amont, l'avis PC en aval.

---

## 34. Rapport G2AVP

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport d'étude géotechnique G2 AVP** (Avant-Projet) selon la norme NF P 94-500. Étude réalisée par un bureau d'études géotechnique pour caractériser le sol et fonder le dimensionnement des structures (pieux battus, plots béton, vis ancrées).

**Format observé** : PDF, 30-80 pages avec annexes (sondages, essais), tableaux et coupes géotechniques.

**Indices internes typiques** :
- **Page de garde** : logo BE géotechnique, titre "Étude géotechnique G2 AVP" ou "Mission G2 Avant-Projet", code projet, commune, date
- **Référence norme** : "NF P 94-500"
- **Sections** : Contexte, Méthodologie (sondages, essais pressiométriques), Résultats des essais, Caractérisation des sols, Recommandations fondations
- **Tampon BE + signature ingénieur géotechnicien**

**Nommage probable** : `Rapport_G2AVP_[BE]_[CodeProjet]_[date].pdf`.

**Piège** : ne pas confondre avec le rapport G2PRO (doc #64, J3) qui est plus poussé. G2 AVP < G2 PRO en niveau de détail.

---

## 35. Rapport étude pédologique / ZH / Faune et Flore / EIE

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Document regroupant les rapports environnementaux** : étude pédologique, zones humides, inventaires faune et flore, et étude d'impact environnemental (EIE). **Peut être un seul gros rapport ou plusieurs rapports séparés** selon le BE. Ce sont les **livrables** des études commandées via le devis Enviro (doc #13) — à ne PAS confondre avec le rapport EPA final (doc #36) qui est une étude agricole et économique.

**Format observé** : PDF, 100-300+ pages selon ampleur (rapport unique) ou plusieurs PDF (rapports séparés par thématique).

**Indices internes typiques** :
- **Page de garde** : logo BE environnemental (Biotope, Calidris, Egis, Naldéo, etc.) + EnerVivo client + titre "Volet Naturel de l'Étude d'Impact" / "VNEI" / "Inventaires faune-flore et zones humides"
- **Cadre réglementaire** : références Code de l'environnement (R. 122-2, L. 411-1, L. 211-1), arrêté du 24 juin 2008 sur les zones humides. **PAS de mention CDPENAF ni Décret 2016-1190 (ce sont des marqueurs EPA)**
- **Sections typiques** :
  - Pédologie / Zones humides : sondages pédologiques, classification GEPPA, délimitation des ZH
  - Faune : inventaires 4 saisons (oiseaux, mammifères, chiroptères, reptiles, amphibiens, insectes)
  - Flore et habitats : relevés phytosociologiques, cartographie habitats EUNIS/Natura 2000
  - Évaluation des impacts et Mesures ERC (Éviter, Réduire, Compenser)

**Nommage probable** : `Rapport_VNEI_[BE]_[CodeProjet]_S[X]_[date].pdf`, `EIE_complete_[CodeProjet].pdf`, `Etude_FFH_ZH_[CodeProjet].pdf`.

**Pièges** :
1. **Plusieurs versions saisons** : Saison 1 (printemps/été) puis Saison 2 (automne/hiver) → VNEI complet après 4 saisons. LLM marque Présent dès qu'au moins le rapport VNEI ou EIE final est trouvé.
2. **Ne PAS confondre avec le rapport EPA** : l'EPA parle d'économie agricole, de CDPENAF, de compensation collective — l'EIE/VNEI parle d'espèces protégées, zones humides, habitats naturels.

---

## 36. Rapport EPA final

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**[V13 - Précision renforcée] Livrable final de l'Étude Préalable Agricole** (EPA) — rapport complet émis par le bureau d'études agricole, répondant aux exigences du **Décret n° 2016-1190** et de l'article **L. 112-1-3 du Code rural**. Cas par cas : obligatoire uniquement si emprise > seuil départemental (défaut 5 ha) en zone agricole.

**🚨 Qu'est-ce que l'EPA ?** L'EPA est une **étude technico-économique** analysant l'impact du projet photovoltaïque sur l'**économie agricole locale** : emplois agricoles affectés, productions animales et végétales, filières agroalimentaires, foncier agricole consommé, compensation agricole collective à prévoir. Elle NE porte PAS sur la faune, la flore, les zones humides ou les paysages — ce sont des sujets couverts par l'EIE/VNEI (doc #35).

**Discrimination EPA vs EIE/VNEI** :
- **EPA** → termes clés : "Étude Préalable Agricole", "EPA", "CDPENAF", "Décret 2016-1190", "économie agricole", "compensation collective agricole", "article L. 112-1-3 Code rural", "impact sur les exploitations agricoles"
- **EIE/VNEI** → termes clés : "Volet Naturel", "VNEI", "étude d'impact", "faune", "flore", "habitats", "zones humides", "espèces protégées", "Code de l'environnement"

**Format observé** : PDF, 80-200 pages avec annexes.

**Indices internes typiques** :
- **Page de garde** : logo BE agricole (Artifex, Naldéo, Agroconsult, etc.) + EnerVivo client + titre **"Étude Préalable Agricole"** + code projet + commune + département + date
- **Cadre réglementaire** : références **Décret 2016-1190**, article L. 112-1-3 Code rural, **CDPENAF**
- **Sections obligatoires** (article D. 112-1-19) :
  1. Description du projet et délimitation du territoire d'étude
  2. État initial de l'économie agricole du territoire (productions, filières, emplois, structures d'exploitations)
  3. Effets positifs et négatifs sur l'économie agricole + évaluation financière des impacts
  4. Mesures d'évitement et de réduction
  5. Mesures de compensation collective agricole (montants, modalités)
- **Cartographies** : parcellaire, occupation des sols agricoles, sols pédologiques (à ne pas confondre avec l'analyse de biodiversité de l'EIE)
- **Annexes** : entretiens avec exploitants agricoles, données INSEE/RGA (Recensement Général Agricole), statistiques agricoles départementales

**Nommage probable** : `Rapport_EPA_[BE]_[CodeProjet]_v[X].pdf`, `Etude_prealable_agricole_[Commune]_[date].pdf`.

**Pièges** :
1. **Ne PAS confondre avec le rapport EIE/VNEI** (doc #35) — le rapport EPA ne contient pas d'inventaires naturalistes
2. **Ne PAS confondre avec le devis EPA** (doc #12, J2a) — le devis fait 20-30 pages, le rapport final fait 80-200+ pages
3. **Cas par cas** : si emprise sous seuil, EPA non requis (N/A)

---

## 37. Étude architecte

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Étude architecturale** obligatoire si la surface de plancher du projet > 150 m². Réalisée par un architecte inscrit à l'Ordre des Architectes. Souvent **N/A** pour les centrales PV sol (pas de surface de plancher au sens du Code de l'urbanisme).

**Format observé** : PDF mêlant texte et plans architecturaux.

**Indices internes typiques** :
- **Cartouche architecte** : nom de l'agence, numéro d'inscription Ordre des Architectes (NCI)
- **Sections** : Notice descriptive (PC4), insertion paysagère (PC5, PC6), plans (PC2, PC3), perspectives (PC7, PC8)
- **Référence Code de l'urbanisme** : article L. 431-1 (recours obligatoire à un architecte)

---

## 38. Rapport géomètre

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Document du géomètre-expert attestant du bornage et de la délimitation précise des parcelles du projet. Inclut plan topographique, niveaux altimétriques, limites cadastrales et procès-verbaux de bornage.

**Format observé** : PDF + DWG, document multi-pages 10-30 pages.

**Indices internes typiques** :
- **Cartouche géomètre** : nom du cabinet, inscription OGE (Ordre des Géomètres-Experts)
- **Titre** : "Plan de bornage", "Plan topographique", "PV de bornage contradictoire"
- **Contenu** : courbes de niveau, limites parcellaires, bornes posées, table des superficies

**Piège** : distinguer le **plan de bornage** (acte les limites) du **simple relevé topographique** (mesure le terrain).

---

## 39. Attestation cas par cas validé

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Décision de la DREAL** suite à examen au cas par cas (article R. 122-3 du Code de l'environnement), précisant si le projet est soumis à étude d'impact environnementale ou non.

**Format observé** : PDF officiel DREAL/Préfecture, 5-15 pages.

**Indices internes typiques** :
- **En-tête** : République Française + logo DREAL ou Préfecture
- **Titre** : "Décision d'examen au cas par cas" ou "Arrêté préfectoral - examen cas par cas"
- **Conclusion clé** : "Le projet [n']est [pas] soumis à étude d'impact"
- **Signature** : Préfet ou Directeur DREAL par délégation

**Stratégie** :
1. Si document = **décision DREAL signée avec date de notification** → cas par cas validé ✓
2. Si seulement la **demande déposée** (pas encore de réponse) → flag Ambigu "Saisine déposée, décision DREAL en attente"

---

## 40. PRAC reçue

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**PRAC = Proposition de Raccordement Avant Complétude de la demande**. Document adressé par Enedis au Demandeur (EnerVivo / SPV), **après paiement d'un devis préalable**, fournissant une estimation préliminaire des conditions techniques et financières du raccordement. Étape précoce antérieure à la PTF définitive (cf. doc #58).

**Format observé** : PDF officiel Enedis, 5-20 pages.

**Indices internes typiques** :
- **Titre** : "Proposition de Raccordement Avant Complétude" ou "PRAC"
- **Mention** : "demande anticipée", référence délibération CRE n° 2019-66 du 21 mars 2019
- **Contenu** : puissance demandée (kVA), point de raccordement envisagé, coût estimé, **délai prévisionnel de mise en exploitation**

**Stratégie (PRAC vs PTF)** :
1. Mention **"Avant Complétude"** ou "demande anticipée" → PRAC (doc #40, J2b)
2. Mention **"Proposition Technique et Financière" finale** sans référence à l'anticipation → PTF (doc #58, J3)

---

## 41. Arrêté municipal passage des parcelles en ZAENR

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Arrêté municipal** délibérant le passage des parcelles en **Zone d'Accélération des Énergies Renouvelables** (ZAENR) — dispositif issu de la Loi n° 2023-175 du 10 mars 2023 (article 15).

**Format observé** : PDF, arrêté ou délibération municipale, 2-5 pages.

**Indices internes typiques** :
- **En-tête** : Mairie de [Commune], République Française
- **Titre** : "Délibération du Conseil Municipal" + "Zone d'Accélération des Énergies Renouvelables" / "ZAENR"
- **Référence loi** : "Loi n° 2023-175 du 10 mars 2023 (...) article L. 141-5-3 du Code de l'énergie"
- **Signature maire** + tampon de mairie

**Piège** : pas tous les projets ont ZAENR (toutes les communes n'en ont pas encore défini) → si absent, marquer N/A.

---

## 42. Récépissé dépôt PC ou DP

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Récépissé officiel** de dépôt du dossier de **Permis de Construire** (PC) ou de **Déclaration Préalable** (DP) en mairie. Document court avec **cachet de la mairie** confirmant la prise en compte du dossier.

**Format observé** : PDF scanné, 1-2 pages, formulaire CERFA tamponné.

**Indices internes typiques** :
- **En-tête CERFA** : formulaire CERFA n° 13409*XX (PC) ou n° 13404*XX (DP)
- **Titre** : "Récépissé de dépôt" ou "Accusé de réception d'un dossier de permis de construire"
- **Cachet mairie** : tampon avec nom de la commune + date de dépôt
- **Numéro de dossier** : `PC [INSEE] [Année] [N°]` ou `DP [INSEE] [Année] [N°]`
- **Mention** : "Le délai d'instruction est de [X] mois à compter de cette date"

**Piège** : ne pas confondre avec l'arrêté de PC (qui vient à l'instruction finalisée, en J3). Le récépissé n'est que la **preuve de dépôt**, pas une autorisation.

---

## 43. Projet de bail (notaire)

- **Jalon** : J2b
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Projet de bail emphytéotique rédigé par le notaire, sous forme de **draft pré-signature**. Permet de valider les termes juridiques avant la signature solennelle (bail définitif signé en J3, cf. doc #56).

**Format observé** : PDF, 25-40 pages. Titre "BAIL EMPHYTEOTIQUE" (et non "PROMESSE DE BAIL"). Durée 25-40 ans. **Mention "Projet" ou "Draft"** et absence de signatures des parties.

**Stratégie** :
1. Mention "Projet" et pas de signatures parties → projet de bail (J2b) ✓
2. Signatures des deux parties + mention "Acte authentique" → bail signé (J3, doc #56) ✓

---

## 44. Plan de masse version J2b

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2b du Plan de masse — version "dépôt PC", mêmes principes que J1/J2a (cf. docs #3, #15). Indices de jalon :
- **Cartouche** : `Phase : APD` confirmé, parfois `EXE` selon convention
- **Indice de révision** : typiquement `Ind C` (ou `Ind B` si nomenclature compacte)
- **Mention "dépôt PC/DP"** : c'est le plan de masse joint au dossier de permis de construire

---

## 45. TADD version J2b

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2b du TADD — mêmes principes que J1/J2a (cf. docs #4, #16). Spécificités :
- Hypothèses **figées pour le dépôt PC** : modèle de modules définitif, structures choisies, raccordement chiffré (PRAC reçue)
- Jalon `J2B` ou `J2b` dans le nom (ex : `250909_TADD_v6_6_DVAUJANY_J2B_JSW.xlsm`)

---

## 46. Dossier de qualification J2b

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2b du Dossier de qualification — mêmes principes que J1/J2a (cf. docs #5, #30). Contenu spécifique J2b :
- **Jalon `J2b` explicite dans le nom** (ex : `260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx`)
- Intègre : avis instances (DDT, SDIS, ZAENR), rapports environnementaux (VNEI), G2 AVP, géomètre, plan de masse APD, TADD J2b, dossier PC déposé

---

# J3 — Préparation Ready to Build

## 47. ANRNR

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**ANRNR = Attestation de Non-Recours et de Non-Retrait** délivrée par la mairie après purge complète des délais de recours contre le permis de construire. **Document central pour la sécurité juridique du projet.**

**Format observé** : PDF officiel mairie, 1-2 pages.

**Indices internes typiques** :
- **Titre** : "Attestation de non-recours et de non-retrait" ou "Certificat de non-recours"
- **Mention clé** : "atteste qu'aucun recours n'a été enregistré dans les délais légaux de [2 mois pour PC / 1 mois pour DP]"
- **Mention** : "et que la décision n'a pas fait l'objet d'un retrait"
- **Signature maire** + **tampon mairie**

**Nommage probable** : `ANRNR_[CodeProjet]_[date].pdf`, `Attestation_non_recours_[Commune].pdf`.

---

## 48. Avis CDPENAF

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Avis de la Commission Départementale de Préservation des Espaces Naturels, Agricoles et Forestiers** (CDPENAF). Instance consultative obligatoire pour les projets en zone agricole (articles L. 112-1-1, L. 112-1-2 du Code rural).

**Format observé** : PDF officiel préfecture, 3-10 pages.

**Indices internes typiques** :
- **Titre** : "Avis de la CDPENAF" ou "Procès-verbal de la CDPENAF"
- **Sections** : Présentation du dossier, Analyse de l'EPA, Évaluation des effets, **Avis final** (favorable / défavorable / réservé)
- **Position sur la compensation** : montants, modalités

**Piège** : vérifier le sens de l'avis — si défavorable → blocage projet probable.

---

## 49. PV 1er passage huissier

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

**Procès-verbal dressé par un commissaire de justice** (ex-huissier) constatant l'affichage du permis de construire sur le terrain — 1er passage, typiquement juste après affichage. Ces PV démontrent la **continuité de l'affichage** pendant les 2 mois de délai de recours, pour sécuriser l'ANRNR.

**Format observé** : PDF officiel commissaire de justice, 3-10 pages.

**Indices internes typiques** :
- **En-tête** : "Étude de Maître [Nom], Commissaire de Justice" (ex-huissier)
- **Titre** : "Procès-verbal de constat" ou "PV de constat d'affichage"
- **Mention objet** : "constat d'affichage du permis de construire n° [PC...]"
- **Contenu** : description du panneau (dimensions, contenu, état, localisation GPS), **photos jointes**

**Stratégie** : distinguer les 3 PV par ordre chronologique (le plus ancien = 1er passage).

---

## 50. PV 2ème passage huissier

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Identique au doc #49, 2ème passage environ 30 jours après le 1er. Même format, même structure. Date de constat postérieure d'environ 1 mois au 1er passage.

---

## 51. PV 3ème passage huissier

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Identique aux docs #49-50, 3ème et dernier passage en fin de période de recours. Date de constat postérieure d'environ 2 mois au 1er passage. Clôture la preuve de continuité d'affichage.

---

## 52. Présentation de la création SPV à la mairie

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Présentation faite par EnerVivo à la mairie pour annoncer la **création de la Société de Projet (SPV)**. Étape de communication politique avec les élus locaux.

**Format observé probable** : `.pptx` ou PDF de présentation, 10-30 slides.

**Indices internes typiques** :
- **Charte EnerVivo** (logo, couleurs vert/jaune)
- **Titre** : "Création de la SPV [Nom projet]" ou "Présentation à la commune de [...]"
- **Slides typiques** : rappel du projet, structure juridique SPV, actionnariat, calendrier, retombées locales (taxes foncières, IFER)

**Piège** : ne pas confondre avec le dossier de qualification (interne VivEpic). Cette présentation est externe (destinée à la mairie).

---

## 53. Kbis SPV

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Extrait Kbis de la **Société de Projet (SPV)** nouvellement créée pour porter le projet PV. Mêmes caractéristiques formelles que le Kbis du propriétaire (cf. doc #20) mais pour la SPV d'exploitation.

**Spécificité SPV** :
- Dénomination typique : "Centrale [Nom projet]" ou "[Code projet] Énergies" ou "SAS [Nom commune]"
- Forme juridique : SAS le plus souvent
- **Objet social** : "Production et vente d'électricité d'origine photovoltaïque"
- **Présidence** : EnerVivo représenté par Sylvain FREDERIC ou habilité

**Piège** : à distinguer du Kbis du propriétaire foncier (doc #20). Le Kbis SPV est récent (postérieur à la création de la SPV en J3).

---

## 54. Statuts SPV signés

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Statuts signés de la **Société de Projet (SPV)**. Mêmes caractéristiques formelles que les statuts du propriétaire (cf. doc #19) mais pour la SPV d'exploitation.

**Spécificités SPV** :
- **Objet social** : "L'étude, la conception, le développement, le financement, la construction, l'exploitation, la maintenance, l'achat et la vente d'électricité d'origine photovoltaïque"
- **Présidence** : EnerVivo (personne morale) ou Sylvain FREDERIC

**Piège** : à distinguer des statuts du propriétaire foncier (doc #19).

---

## 55. Pacte d'actionnaires signé

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Pacte d'actionnaires signé entre les associés de la SPV régissant leurs relations (gouvernance, sortie, préemption, distribution de dividendes). Document confidentiel complémentaire aux statuts.

**Format observé** : PDF, 20-50 pages.

**Indices internes typiques** :
- **Titre** : "Pacte d'actionnaires" ou "Pacte d'associés" ou "Shareholders Agreement"
- **Sections typiques** : Objet, Gouvernance, Décisions importantes, Droits de cession, Sortie, Confidentialité
- **Signatures de tous les associés** en fin de document

**Piège** : document **confidentiel** — marquer Présent sans détailler les clauses.

---

## 56. Bail signé (acte notarié)

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Bail emphytéotique définitif signé par acte notarié authentique** entre le Promettant (propriétaire foncier) et la SPV. Durée typique 25-40 ans.

**Format observé** : PDF, 30-50 pages, **acte notarié authentique**.

**Indices internes typiques** :
- **En-tête** : Office Notarial, "Maître [Nom], Notaire"
- **Titre** : "BAIL EMPHYTEOTIQUE" (et non "PROMESSE DE BAIL")
- **Mention** : "Acte authentique" ou "Acte reçu par Maître [...]"
- **Durée** : 25 ans typiquement (max 99 ans selon Code rural L. 451-1)
- **Signatures** : Bailleur + Emphytéote (SPV) + Notaire

**Pièges** :
1. Drafts à ignorer — seul l'acte avec signatures notariales et mention "acte authentique" valide le jalon
2. L'Emphytéote doit être la SPV (et non EnerVivo en direct), conformément à la clause de substitution de la PDB

---

## 57. Récépissé de la demande de raccordement / CRD

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Récépissé / accusé de réception de la **demande de raccordement** déposée par la SPV auprès d'Enedis.

**Format observé** : PDF Enedis, 1-3 pages.

**Indices internes typiques** :
- **Titre** : "Accusé de réception" ou "Récépissé de demande de raccordement"
- **Mention** : "Votre demande de raccordement a été enregistrée"
- **Identification demandeur** : SPV (et non EnerVivo)

---

## 58. PTF / CRD reçue d'ENEDIS

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

**PTF = Proposition Technique et Financière** émise par Enedis pour le raccordement de la centrale au réseau. Document détaillant les modalités techniques et le **coût du raccordement** (non encore signé à ce stade).

**Format observé** : PDF Enedis officiel, 20-50 pages avec schémas.

**Indices internes typiques** :
- **Titre** : "Proposition Technique et Financière" ou "PTF"
- **Sections** : Caractéristiques du raccordement, Travaux côté Enedis, Travaux côté producteur, Coût total HT, Délais de validité

---

## 59. PTF / CRD signée

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**PTF/CRD signée** par la SPV — acceptation par la SPV de la proposition Enedis. **Engagement contractuel ferme** entre la SPV et Enedis.

**Format et indices** : identiques au doc #58 (PTF reçue), mais avec :
- **Signature SPV** sur la PTF ("bon pour accord, lu et approuvé")
- **Confirmation du versement d'acompte** (souvent 30% du montant total)

**Piège** : seule la version signée valide le jalon — drafts à ignorer.

---

## 60. CRD transférée VivEpic vers SPV

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Document actant le **transfert de la Convention de Raccordement et Distribution** (CRD) de VivEpic vers la SPV. Étape administrative pour que la SPV devienne titulaire du raccordement Enedis.

**Format observé** : PDF, document Enedis ou avenant, 2-5 pages.

**Indices internes** : Ancien titulaire : VivEpic. Nouveau titulaire : SPV [Code projet]. Signatures des deux parties + Enedis.

---

## 61. Consultations / Devis auprès des fournisseurs

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Ensemble des **consultations et devis** reçus des fournisseurs et sous-traitants pour la construction : EPC, modules PV, onduleurs, structures, transformateurs, génie civil, raccordement HTA, etc.

**Format observé** : multiples PDF. **Multi-fichiers** par nature.

**Localisation** : `7-Achat-Fournisseurs/1-Consultations/`.

**Stratégie** : LLM marque "Présent" dès qu'au moins 1-2 devis fournisseurs sont trouvés.

---

## 62. CETI

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**CETI = Certificat d'Éligibilité du Terrain d'Implantation**. Certificat délivré par **le préfet de région**, attestant de l'éligibilité d'un terrain pour l'implantation d'une centrale PV dans le cadre des **appels d'offres CRE**. **Obligatoire pour candidater aux AO CRE > 500 kWc**.

**Format observé** : PDF officiel préfecture de région, 3-10 pages.

**Indices internes typiques** :
- **Titre** : "Certificat d'Éligibilité du Terrain d'Implantation" ou "CETI"
- **Décision préfectorale** : éligibilité confirmée avec **catégorisation du terrain** (zones urbanisées / sites dégradés / zones agricoles)
- **Notation** : note attribuée selon la grille du cahier des charges de l'AO CRE concerné

**Stratégie** :
1. Projet < 500 kWc OU pas d'AO CRE → CETI N/A
2. Projet > 500 kWc avec candidature AO CRE → CETI obligatoire

---

## 63. Candidature tarif d'achat (AO CRE, AOS, S21, ACC)

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Dossier de candidature pour bénéficier d'un **tarif d'achat de l'électricité** via un appel d'offres ou un guichet ouvert : AO CRE, AOS, S21 (< 500 kWc), ACC (autoconsommation collective).

**Format observé** : dossier multi-documents PDF, plusieurs dizaines de pages.

**Indices internes typiques** :
- **Référence CRE** : numéro de période d'AO, famille tarifaire (T1, T2, T3, T4 selon puissance)
- **Pièces du dossier** : note descriptive, plan d'implantation, justificatifs fonciers, **prix de vente proposé (€/MWh)**

---

## 64. Rapport G2PRO

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Rapport d'étude géotechnique G2 PRO** (Projet) selon la norme NF P 94-500 — version plus poussée que la G2 AVP (cf. doc #34). Réalisée typiquement **après obtention du PC et avant lancement construction**.

**Format et indices** : similaire au doc #34, avec différences :
- **Titre** : "Étude géotechnique G2 PRO" ou "Mission G2 Projet"
- **Référence norme** : "NF P 94-500 - Phase G2 PRO"
- **Niveau de détail accru** : calculs de dimensionnement fondations détaillés (descente de charge par pieu/plot)

**Piège** : distinguer de la G2 AVP (doc #34, J2b). G2 PRO arrive en J3, plus détaillée.

---

## 65. Plan de masse version J3

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J3 du Plan de masse — mêmes principes que précédents (cf. docs #3, #15, #44). Spécificités J3 :
- **Cartouche** : `Phase : EXE` (Exécution) ou `PRO` (Projet)
- **Indice de révision** : typiquement `Ind D`
- **Version "Pré-Ready to Build"** : intègre les retours G2 PRO, implantation définitive des fondations

---

## 66. TADD version J3

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J3 du TADD — mêmes principes que précédents. Spécificités :
- Hypothèses **finalisées pour le closing bancaire** à venir (J4)
- Intègre : PTF Enedis signée, devis EPC consolidés, tarif d'achat retenu (post-candidature CRE)
- TRI / VAN définitifs pour validation comité d'investissement

---

## 67. Dossier de qualification J3

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J3 du Dossier de qualification — mêmes principes que précédents. Contenu J3 :
- **Jalon `J3` explicite dans le nom**
- Intègre : ANRNR, avis CDPENAF, PV huissiers, SPV créée (Kbis, statuts, pacte), bail signé, raccordement Enedis (PTF signée), G2 PRO, candidature tarif d'achat

---

# J4 — Montage économique

## 68. Contrat d'achat d'électricité signé

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Contrat de vente d'électricité signé** entre la SPV (vendeur) et un acheteur (EDF OA pour tarif réglementé, ou agrégateur/fournisseur privé pour PPA). Définit les conditions de vente : prix (€/MWh), durée (15-20 ans), modalités.

**Format observé** : PDF, 30-80 pages.

**Indices internes typiques** :
- **Cas EDF OA** : émetteur EDF Obligation d'Achat, titre "Contrat d'obligation d'achat", référence tarif ou AO CRE
- **Cas PPA** : émetteur agrégateur, titre "Power Purchase Agreement"
- **Signatures** : SPV + acheteur

---

## 69. Contrat d'agrégation signé

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

Contrat d'agrégation signé entre la SPV et un **agrégateur d'énergie** (pour les projets en complément de rémunération). L'agrégateur assure la vente sur le marché spot et le calcul du complément.

**Indices internes typiques** :
- **Émetteur** : agrégateur (Engie, BayWa r.e., Statkraft, etc.)
- **Titre** : "Contrat d'agrégation" ou "Convention d'agrégation"

---

## 70. Offre bancaire signée

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Term sheet / lettre d'offre indicative** signée entre la SPV et la banque finançante, précisant les conditions principales du financement : montant, durée, taux, garanties, ratios financiers (DSCR).

**Format observé** : PDF, 10-30 pages.

**Indices internes typiques** :
- **Émetteur** : banque (BPCE Énergies Vertes, Crédit Agricole CIB, BNP Paribas, BPI France, etc.)
- **Titre** : "Term Sheet" ou "Offre de financement" ou "Lettre d'engagement"
- **Sections** : Montant (€), Durée (15-18 ans en project finance), Taux, Ratios financiers (DSCR > 1,20 typiquement), Garanties

---

## 71. Closing Bancaire / Documents de crédit signés

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Documents de closing bancaire** : ensemble des contrats de financement signés (Senior Loan Agreement, sûretés, garanties). Étape majeure : déblocage du financement de la construction.

**Format observé** : multiples PDF (10+ documents par closing).

**Documents typiques du closing** :
- Senior Loan Agreement (contrat de prêt senior)
- Actes de nantissement (actions SPV, comptes bancaires, créances futures PPA/CRD)
- Conventions de gestion des comptes (DSRA, Operating account)
- Garanties à première demande des sponsors

**Stratégie** : LLM marque "Présent" dès que les principaux documents (Senior Loan Agreement + actes de nantissement) sont trouvés.

---

## 72. Contrat EPC signé

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

**Contrat EPC = Engineering Procurement Construction** signé entre la SPV et l'entreprise de construction. Contrat clé en main pour la conception, l'approvisionnement et la construction.

**Format observé** : PDF, 50-150 pages avec annexes techniques.

**Indices internes typiques** :
- **Titre** : "Contrat EPC" ou "Engineering Procurement Construction Agreement"
- **Sections** : Objet, Prix forfaitaire, Délais (date COD), Garanties techniques, Pénalités de retard
- **Signatures** : SPV + EPC contractor

---

## 73. Contrat AMO signé

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

**Contrat AMO = Assistance à Maîtrise d'Ouvrage** signé entre la SPV et un AMO indépendant. L'AMO supervise le chantier indépendamment de l'EPC.

**Format observé** : PDF, 20-40 pages.

**Indices internes typiques** :
- **Titre** : "Contrat d'Assistance à Maîtrise d'Ouvrage" ou "AMO Contract"
- **Missions** : validation conception, suivi chantier, OPC, réception, levée des réserves

---

## 74. Devis génie civil signé

- **Jalon** : J4
- **Propriété** : Facultatif
- **Versioning** : Version signée uniquement

### Description

Devis signé pour les **travaux de génie civil** (terrassements, fondations, voiries, clôtures, locaux techniques). Si projet en multi-lots (pas d'EPC global), le génie civil est contracté séparément.

---

## 75. Devis installation centrale PV signé

- **Jalon** : J4
- **Propriété** : Facultatif
- **Versioning** : Version signée uniquement

### Description

Devis signé pour l'**installation de la centrale PV** : fourniture et pose des structures, modules, onduleurs, câbles, transformateurs. Si projet en multi-lots, contrat séparé du génie civil.

---

## 76. Contrat O&M signé

- **Jalon** : J4
- **Propriété** : Facultatif
- **Versioning** : Version signée uniquement

### Description

**Contrat O&M = Operation & Maintenance** signé entre la SPV et un prestataire. Couvre l'exploitation et la maintenance de la centrale (20-30 ans).

**Format observé** : PDF, 30-60 pages.

**Indices internes typiques** :
- **Titre** : "Contrat O&M" ou "Operation & Maintenance Agreement"
- **Sections** : Périmètre (maintenance préventive + curative + monitoring + reporting), Durée, Rémunération, KPI (disponibilité minimale, PR)

---

## 77. CARDi

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**CARDi = Contrat d'Accès au Réseau de Distribution pour l'injection** — contrat régissant l'accès de la SPV au réseau Enedis pour l'injection de l'électricité. Distinct de la PTF (raccordement physique).

**Indices internes typiques** :
- **Émetteur** : Enedis
- **Titre** : "Contrat d'Accès au Réseau de Distribution pour l'Injection" ou "CARDi"
- **Sections** : Objet (accès réseau), Tarif d'utilisation (TURPE), Comptage, Responsabilité d'équilibre

---

## 78. Assurance RC Pro souscrite

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Attestation d'assurance Responsabilité Civile Professionnelle** souscrite par la SPV.

**Format observé** : PDF attestation assureur, 1-2 pages.

**Indices internes typiques** :
- **Titre** : "Attestation d'assurance RC Professionnelle"
- **Identification souscripteur** : SPV [Nom projet]
- **Période de validité** : date début + date fin

---

## 79. Assurance Dommage-Ouvrage (DO)

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Attestation d'assurance **Dommage-Ouvrage** souscrite par la SPV. Garantie décennale construction (10 ans) — obligatoire pour constructions au sens de la loi Spinetta.

**Piège** : pour les centrales PV au sol, l'application du DO est parfois discutée juridiquement (selon que le PV est qualifié de "construction" ou "équipement").

---

## 80. Assurances décennales prestataires

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Attestations d'**assurance décennale** des prestataires intervenant sur le chantier (EPC contractor, génie civil, installateurs PV, électriciens).

**Format observé** : multiples PDF (un par prestataire).

**Stratégie** : LLM marque "Présent" si attestations des principaux prestataires (EPC, GC, électricien) trouvées.

---

## 81. Dossier EXE

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Dossier EXE = Dossier d'Exécution** — ensemble des plans et notes techniques d'exécution permettant la construction effective. Validé avant lancement du chantier.

**Format observé** : multiples fichiers (plans DWG, PDF, notes de calcul, schémas), organisés par lot.

**Contenu typique** :
- Plans d'exécution structures (implantation tables, fondations)
- Plans d'exécution électriques (cheminements câbles, schéma unifilaire détaillé, plan de mise à la terre)
- Notes de calcul (descente de charges, dimensionnement fondations)
- Schémas postes de livraison et de transformation
- **Cartouches** : Phase EXE / Ind A, B, C selon révisions
- **VISA bureau de contrôle** dans cartouche

**Stratégie** : LLM marque "Présent" si au moins le sommaire EXE et quelques plans clés sont trouvés.

---

## 82. Pull out test

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Pull-out test = essai d'arrachement** réalisé sur quelques pieux témoins pour vérifier la capacité d'ancrage des structures. **Préalable au lancement de la fondation en masse**.

**Format observé** : PDF rapport d'essai, 10-30 pages.

**Indices internes typiques** :
- **Titre** : "Rapport d'essais de chargement" ou "Pull-out tests" ou "Essais d'arrachement"
- **Méthodologie** : nombre de pieux testés (typiquement 3-5), profondeur d'enfoncement, charge appliquée par paliers
- **Résultats** : courbes charge/déplacement, valeur de charge limite mesurée vs valeur de calcul
- **Photos** : équipement d'essai sur le terrain

---

## 83. Plan de masse version J4

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J4 du Plan de masse — version **"finale pour construction"**, intégrant les ajustements post-pull-out test et toutes les validations bureau de contrôle. Indices :
- **Cartouche** : `Phase : EXE` confirmé
- **Indice de révision** : typiquement `Ind E` ou plus
- **Statut** : "BPE" (Bon Pour Exécution) ou "DEX" (Document EXécution)
- **VISA bureau de contrôle** dans cartouche

---

## 84. TADD version J4

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J4 du TADD — version **post-closing bancaire**, toutes hypothèses figées. Spécificités :
- Intègre : taux de prêt final, échéanciers, contrats EPC/O&M signés (CAPEX/OPEX définitifs), tarif d'achat retenu
- **Plan d'affaires définitif** pour la SPV — base du suivi exploitation post-MES
- Jalon `J4` dans le nom

---

## 85. Dossier de qualification J4

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J4 du Dossier de qualification — **dernier dossier avant construction**. Contenu :
- **Jalon `J4` explicite dans le nom**
- Intègre : tous les contrats signés (achat électricité, EPC, O&M, AMO), closing bancaire, assurances, dossier EXE validé, pull-out tests
- Slides typiques : "Tour de table financier", "Closing achevé", "Contrats clés signés", "Lancement chantier"

---

# J5 — Construction

## 86. Déclaration d'Ouverture de Chantier (DOC)

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Déclaration d'Ouverture de Chantier (DOC)** déposée en mairie par la SPV pour notifier officiellement le démarrage des travaux (article R. 424-16 du Code de l'urbanisme).

**Format observé** : PDF formulaire CERFA tamponné, 1-2 pages.

**Indices internes typiques** :
- **En-tête CERFA** : formulaire CERFA n° 13407*XX
- **Titre** : "Déclaration d'ouverture de chantier"
- **Référence PC** : numéro du permis de construire concerné
- **Cachet mairie** : tampon avec date de dépôt

---

## 87. Plans d'exécution validés

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

**Plans d'exécution validés** par l'AMO et le bureau de contrôle, à jour pour le chantier. Évoluent pendant le chantier avec des révisions (Ind A → Ind B → Ind C…) suite aux adaptations terrain.

**Indices internes typiques** :
- **Cartouche** : `Phase : EXE`, indice révision, **mention "BPE" (Bon Pour Exécution)**
- **Validation** : VISA AMO + VISA bureau de contrôle dans cartouche
- **Date de validation** récente (postérieure à la DOC)

**Stratégie** : LLM marque "Présent" si plans EXE récents et validés (postérieurs à la DOC).

---

## 88. Rapport bureau de contrôle (VISA)

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport du bureau de contrôle technique** (Apave, Veritas, Socotec, Dekra, Qualiconsult) attestant de la conformité des plans d'exécution et des travaux aux normes techniques.

**Format observé** : PDF officiel bureau de contrôle, 10-30 pages.

**Indices internes typiques** :
- **En-tête bureau de contrôle** : logo Apave / Bureau Veritas / Socotec / Dekra / Qualiconsult
- **Titre** : "Rapport de contrôle" ou "Rapport initial de contrôle technique"
- **VISA** : tableau récapitulatif des plans visés (numéro, indice, statut Validé/Refusé/Réserves)
- **Signature** : contrôleur technique habilité

---

## 89. Certification carbone des modules

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Certificat d'évaluation carbone des modules** PV installés, requis pour les appels d'offres CRE imposant un critère carbone (typiquement < 550 kg eqCO2/kWc).

**Format observé** : PDF certificat, 5-15 pages.

**Indices internes typiques** :
- **Émetteur** : fabricant des modules ou organisme certificateur (Certisolis, etc.)
- **Titre** : "Évaluation carbone simplifiée" ou "ECS" ou "Certification empreinte carbone modules PV"
- **Valeur carbone** : kg eqCO2 / kWc
- **Conformité** : mention "Conforme au cahier des charges de l'AO CRE [...]"

---

## 90. Agréments et décennales installateurs

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Ensemble des **agréments professionnels et attestations décennales** des installateurs intervenant sur le chantier (qualifications QualiPV, Qualifelec, Quali'EnR, OPQIBI, FFB, et décennales).

**Format observé** : multiples PDF.

**Indices internes typiques** :
- **Agréments** : certificats QualiPV ("RGE - Reconnu Garant Environnement"), Qualifelec, Quali'EnR
- **Décennales** : attestations assureur par prestataire

---

## 91. Déclarations de sous-traitance

- **Jalon** : J5 (Construction)
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Déclarations de sous-traitance déposées par l'EPC contractor auprès de la SPV pour valider chaque sous-traitant. Conforme à la **loi du 31 décembre 1975** relative à la sous-traitance.

**Format observé** : multiples formulaires CERFA ou documents équivalents.

---

## 92. Planning chantier

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Planning détaillé du chantier** (Gantt) émis par l'EPC contractor ou l'AMO. Précise les phases de construction avec dates de début/fin et jalons clés.

**Format observé** : PDF (extrait MS Project ou équivalent), 1-10 pages.

**Contenu typique** : phases (préparation, terrassement, fondations, structures, modules, électricité, raccordement, mise en service), jalons (DOC, Pull-out test, première table installée, COD, réception).

---

## 93. Plan QHSE

- **Jalon** : J5 (Construction)
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Plan QHSE = Qualité, Hygiène, Sécurité, Environnement** du chantier. Document encadrant les mesures de prévention des risques pendant la construction.

**Format observé** : PDF, 20-50 pages.

**Indices internes typiques** :
- **Titre** : "Plan QHSE" ou "Plan Particulier de Sécurité et de Protection de la Santé" (PPSPS) ou "Plan général de coordination" (PGC)
- **Référence** : article L. 4532-1 et suivants Code du travail

---

## 94. Architecture SCADA

- **Jalon** : J5 (Construction)
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Architecture du SCADA** (Supervisory Control And Data Acquisition) — schéma technique du système de supervision et télégestion de la centrale.

**Format observé** : PDF schémas + notes, 10-30 pages.

**Indices internes typiques** :
- **Schémas** : architecture réseau SCADA, position des capteurs, équipements de communication (PLC, routeurs, modems 4G), liaison avec serveurs centralisés
- **Émetteur** : EPC contractor ou intégrateur SCADA (Solar-Log, Skytron, Meteocontrol, etc.)
- **Référence protocoles** : Modbus TCP, IEC 61850, MQTT, etc.

---

# J6 — Mise en Service (MES)

## 95. CONSUEL

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Attestation CONSUEL** (Comité National pour la Sécurité des Usagers de l'Électricité) — visa de conformité de l'installation électrique. **Préalable obligatoire à la mise en service** par Enedis.

**Format observé** : PDF attestation officielle CONSUEL, 1-3 pages.

**Indices internes typiques** :
- **En-tête** : logo CONSUEL, "République Française"
- **Titre** : "Attestation de conformité" + type (vert pour photovoltaïque)
- **Type d'attestation** : "AC23" (PV avec injection) ou "AC25"
- **Mention** : "Cette attestation est valable pour la mise en service par le gestionnaire de réseau"

**Piège** : pour les centrales > 36 kVA, l'attestation CONSUEL doit être visée par un organisme agréé.

---

## 96. Attestation de conformité ENEDIS et DEIE

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Document fusionné** regroupant deux attestations :
1. **Attestation de conformité Enedis** : Enedis valide la conformité du raccordement
2. **DEIE** (Demande d'Établissement / Déclaration d'Exploitation de l'Installation Électrique) — attestation que l'installation est prête à fonctionner

**Format observé** : PDF Enedis officiel, 2-5 pages.

**Indices internes typiques** :
- **En-tête Enedis**
- **Mention** : "Installation conforme aux exigences de raccordement", "Date de mise en service technique"
- **Caractéristiques validées** : puissance crête, puissance d'injection (kVA), tension, comptage installé

---

## 97. PV de réception chantier

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Procès-verbal de réception du chantier** signé entre la SPV (maître d'ouvrage) et l'EPC contractor. Acte la livraison de la centrale et déclenche la garantie de parfait achèvement (1 an).

**Format observé** : PDF, 5-20 pages avec annexes.

**Indices internes typiques** :
- **Titre** : "Procès-verbal de réception" ou "PV de réception des travaux"
- **Parties** : SPV (réceptionnaire) + EPC contractor + AMO (témoin)
- **Cas possibles** : réception sans réserves / avec réserves (cas le plus courant) / refus de réception
- **Référence article 1792-6 du Code civil**
- **Signatures** : SPV + EPC contractor + AMO

**Piège** : version signée uniquement — drafts à ignorer.

---

## 98. DOE

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**DOE = Dossier d'Ouvrages Exécutés** — ensemble des plans tels qu'exécutés (versions "as-built"), notices techniques, fiches d'équipements, garanties fabricants, schémas électriques définitifs. **Livré par l'EPC contractor à la réception**.

**Format observé** : dossier multi-fichiers, souvent organisé en sous-dossiers : Plans, Notices, Garanties, etc.

**Indices internes typiques** :
- **Titre** : "DOE" ou "Dossier des Ouvrages Exécutés"
- **Cartouche plans** : "TQE" (Tel Que Exécuté) ou "AB" (As-Built)
- **Sommaire structuré** : Plans, Notices techniques, Garanties fabricants, PV d'essais

**Stratégie** : LLM marque "Présent" si dossier DOE structuré trouvé avec sommaire et plans as-built.

---

## 99. Rapport tests PR

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport de tests du Performance Ratio (PR)** — mesure de la performance de la centrale post-MES (productible réel / productible théorique). Test réalisé après MES sur une période donnée (typiquement 1 ou 3 mois) pour valider la performance contractuelle. PR > 80-85% typiquement attendu.

**Format observé** : PDF rapport technique, 20-50 pages.

**Indices internes typiques** :
- **Émetteur** : AMO ou bureau de mesures indépendant
- **Titre** : "Rapport de test Performance Ratio" ou "Test de garantie PR"
- **Méthodologie** : référence **IEC 61724-1** (norme internationale mesure performance PV)
- **Données collectées** : production électrique (kWh), irradiance (kWh/m²), température modules, disponibilité onduleurs
- **Calcul PR** : formule + résultat en %

---

## 100. Rapport tests onduleurs

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**[V13 - Précision] Rapport des tests fonctionnels de mise en route (commissioning tests) réalisés sur les onduleurs** lors de la mise en service de la centrale. Ce ne sont **PAS des tests harmoniques** — il s'agit de tests fonctionnels vérifiant le bon fonctionnement individuel de chaque onduleur avant la mise en exploitation commerciale.

**Objectif des tests** : vérifier que chaque onduleur :
- Démarre et s'arrête correctement (séquence de démarrage/arrêt)
- Produit bien de l'énergie avec le rendement attendu
- Régulations et protections électriques opérationnelles (protection de découplage, détection d'îlotage, coupure sur défaut DC/AC)
- Communication SCADA fonctionnelle (protocole Modbus TCP / RS485 / IEC 61850 selon équipement)
- Paramètres de réglage conformes aux exigences d'injection réseau (cos φ, Q/U, P/f)

**Format observé** : PDF rapport, 10-50 pages avec **tableau de résultats par onduleur**.

**Indices internes typiques** :
- **Émetteur** : installateur électrique, AMO ou fabricant (SUNGROW, SMA, Huawei — service commissioning)
- **Titre** : "Rapport de mise en service onduleurs" ou "Commissioning report" ou "Rapport de tests fonctionnels onduleurs" — **pas** "test harmonique" ni "analyse harmonique"
- **Tableau de tests** : pour chaque onduleur identifié par sa **référence/numéro de série** :
  - Résultat test démarrage : OK/NOK
  - Puissance DC mesurée (W) et rendement (%)
  - Tensions AC mesurées (V phase/phase)
  - Fréquence (Hz)
  - Test communication SCADA : OK/NOK
  - Test protections (découplage, surtension, sousension, surintensité) : OK/NOK
- **Bilan global** : nombre d'onduleurs testés, nombre OK, nombre NOK ou à reprendre
- **Photos** : onduleurs installés, équipements de mesure sur site

**Nommage probable** : `Tests_onduleurs_[CodeProjet]_[date].pdf`, `Commissioning_inverters_[CodeProjet].pdf`, `Rapport_mise_en_service_onduleurs_[CodeProjet].pdf`.

**Pièges à éviter** :
1. **Ce n'est pas un test harmonique** : un rapport d'analyse harmonique (THD — Total Harmonic Distortion) est un document différent mesurant la qualité de l'onde sinusoïdale injectée. Le commissioning des onduleurs teste leur fonctionnement, pas la qualité harmonique.
2. **Ne pas confondre avec le rapport tests PR** (doc #99) : le rapport PR mesure la performance globale de la centrale sur une période, les tests onduleurs mesurent individuellement chaque inverter au moment de la mise en service.
3. Document multi-équipements : certains projets peuvent avoir 10, 20, 50+ onduleurs à tester → le rapport peut être volumineux.

---

## 101. DAT

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**DAT = Déclaration Attestant l'Achèvement et la Conformité des Travaux** (DAACT) déposée en mairie par la SPV à la fin de la construction. Formalité obligatoire (article R. 462-1 du Code de l'urbanisme).

**Format observé** : PDF formulaire CERFA tamponné, 1-3 pages.

**Indices internes typiques** :
- **En-tête CERFA** : formulaire CERFA n° 13408*XX
- **Titre** : "Déclaration attestant l'achèvement et la conformité des travaux (DAACT)" ou "DAT"
- **Référence PC** : numéro du PC concerné
- **Mention** : "Les travaux sont conformes au permis de construire délivré"
- **Cachet mairie** : tampon avec date de dépôt

**Piège** : la mairie a 3 mois pour contester. Au-delà, la conformité est tacite.

---

## 102. Première facture EDF OA ou PPA

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Première **facture émise par la SPV** au titre de la vente d'électricité post-MES.

**Format observé** : PDF facture standard.

**Indices internes typiques** :
- **Émetteur** : SPV [Nom projet], SIRET, adresse
- **Destinataire** : EDF OA ou acheteur PPA
- **Quantités** : énergie injectée en kWh ou MWh
- **Montant HT/TTC** : total facturé
- **Numéro de facture** : F[Année]-[N°]

**Piège** : la première facture peut intervenir avec un décalage de quelques mois après la MES (le temps du premier relevé de comptage).

---

# J7 — Clôture (Exploitation et fin de vie)

## 103. Contrat O&M actif avec rapports périodiques

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon (rapports périodiques)

### Description

**Vérification de l'activité du contrat O&M** (cf. doc #76 signé en J4) avec preuve des prestations réalisées via les **rapports périodiques** émis par le prestataire O&M.

**Format observé** : multiples PDF (rapports périodiques), un par période.

**Indices internes typiques** :
- **Titre** : "Rapport O&M mensuel" ou "Rapport trimestriel" + période
- **Sections** : Performance de la centrale (production, PR, disponibilité), Interventions réalisées, Alertes traitées, Recommandations
- **Tableaux KPI** : production attendue vs réelle, PR mensuel, taux de disponibilité

**Stratégie** : LLM marque "Présent" si au moins 2-3 rapports périodiques récents trouvés.

---

## 104. Plan de démantèlement

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Plan de démantèlement** de la centrale en fin d'exploitation. Document précisant les modalités techniques et financières du démontage. Référence légale : **arrêté du 5 juillet 2024** (loi APER) sur les garanties financières.

**Format observé** : PDF, 20-50 pages.

**Indices internes typiques** :
- **Titre** : "Plan de démantèlement" ou "Plan de fin de vie" ou "Décommissioning Plan"
- **Sections** : Description de la centrale, Méthodologie de démantèlement, Tri et recyclage des matériaux (modules, structures, onduleurs, câbles), Garanties financières
- **Référence Arrêté 5 juillet 2024** : tableau de garantie financière en fonction de la puissance MWc

---

## 105. Certificat recyclage panneaux et acier

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Certificats de recyclage** émis par les filières spécialisées après démantèlement effectif :
- **Modules PV** : filière **PV Cycle France** (éco-organisme agréé)
- **Acier / structures** : filière recyclage métaux (ferrailleurs agréés)
- **Câbles cuivre/aluminium** : filière dédiée
- **Onduleurs et équipements électriques** : filière DEEE

**Format observé** : multiples certificats PDF (un par filière).

**Piège** : document attendu seulement **à la fin de l'exploitation effective** (30+ ans après MES). Pour les centrales en exploitation active, ce document est N/A.

---

## 106. PV remise en état agricole

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Procès-verbal de remise en état agricole** du site après démantèlement. Atteste que le terrain a été restitué en état permettant la reprise immédiate de l'activité agricole. Conforme à l'engagement de réversibilité imposé par la Loi APER (article L. 314-36 du Code de l'énergie) et la PDB.

**Format observé** : PDF, 5-15 pages avec photos et constat.

**Indices internes typiques** :
- **Titre** : "Procès-verbal de remise en état" ou "PV de restitution agricole"
- **Parties** : Emphytéote (SPV) + Bailleur (propriétaire foncier) + parfois huissier ou expert agréé
- **Description état initial avant centrale** vs **état final post-démantèlement**
- **Photos avant/après** : preuves visuelles
- **Constat de réversibilité** : sol décompacté, terre arable restituée, équipements démontés
- **Signatures** : Emphytéote + Bailleur + témoin

**Piège** : document **attendu uniquement en fin de vie** de la centrale (25-30 ans post-MES). N/A pour les projets en exploitation active.

---

## Annexe — Classification des Plans de Masse par jalon (patterns de nommage)

**Rappel** : le jalon n'est JAMAIS explicite dans le nom du fichier Plan de Masse. Utiliser les **indices secondaires** dans le nom.

| Pattern dans le nom | Jalon probable | Logique |
|---------------------|----------------|---------|
| `_APS_` | **J1** | APS = Avant-Projet Sommaire = version la plus précoce |
| `_APD_` | **J2a** | APD = Avant-Projet Détaillé = affinage post-J1 |
| `_depot_PC_` ou `_PC0_` ou `_DP_` | **J2b** | Version jointe au dépôt du PC ou DP |
| `_EXE_` ou `_PRO_` | **J3 ou J4** | Phase Exécution ou Projet = versions finales pré-construction |

**Note V13** : les indices de révision (`Ind A`, `Ind B`, `Ind C`...) sont des **marqueurs chronologiques** indépendants des jalons — ne pas utiliser seuls pour déterminer le jalon.

### Stratégie si nom ambigu
1. **Trier par date** : le plan le plus ancien = J1
2. **Chercher dans un dossier `old/` ou `0 - OLD/`** : les versions J1/J2a peuvent y être archivées
3. **En dernier recours** : ouvrir le PDF et lire le cartouche (Phase + date de modification)
