## 34. Compte-rendu RDV SDIS

- **Jalon** : J2b
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Compte-rendu de RDV avec le **Service Départemental d'Incendie et de Secours** (SDIS / pompiers) — autorité consultative sur les questions de sécurité incendie pour les centrales PV (accès engins de secours, défense extérieure contre l'incendie / DECI, citerne SDIS de 120m³ visible dans le plan de masse, déneigement, agencement portails). RDV nécessaire pour les projets sol importants.

**Format observé** : mêmes principes que les autres CR RDV (cf. doc #7-10).

**Indices internes typiques** :
- **Participants** : représentant SDIS du département (Capitaine, Lieutenant), responsable prévention, représentants EnerVivo
- **Sujets** : défense extérieure contre l'incendie (DECI), citerne 120m³, accès engins, portails, signalétique, plans à fournir
- **Décisions** : prescriptions techniques imposées par le SDIS, à intégrer au dossier PC

**Nommage probable** : `CR_RDV_SDIS_[Dept]_[date]`, `CR_SDIS_[Commune]_[date]`.

**Piège** : ne pas confondre avec l'avis SDIS (document officiel d'avis sur le PC) — le CR est interne, l'avis SDIS est administratif.

---

## 35. Avis de cadrage DDTM sur projet ENR

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Avis officiel rendu par la DDT(M)** (Direction Départementale des Territoires / et de la Mer) suite à une demande de cadrage préalable d'EnerVivo sur le projet ENR. Document de pré-instruction administrative qui détaille les attentes de la DDT sur le dossier PC à venir : doctrine locale, points de vigilance, études complémentaires demandées, position sur l'agrivoltaïsme.

**Format observé** : PDF officiel administratif, 3-10 pages.

**Indices internes typiques** :
- **En-tête** : drapeau République Française + logo "Préfecture" / "Direction Départementale des Territoires de [Dept]"
- **Référence dossier** : numéro de cadrage, date de saisine EnerVivo
- **Destinataire** : "SAS ENERVIVO" + adresse Bordeaux
- **Sections** : Contexte, Doctrine locale ENR, Compatibilité PLUi/SCoT, Points d'attention CDPENAF, Études complémentaires demandées, Cadre APER
- **Signature** : Directeur DDT ou chef de service ENR
- **Mention** : "Avis de cadrage / pré-instruction" — n'engage pas formellement la DDT mais oriente le dossier

**Nommage probable** : `Avis_cadrage_DDT[M]_[Dept]_[CodeProjet]_[date].pdf`.

**Localisation** : `4 - Documents Administratifs/Instances` ou `Cadrage`.

**Piège** : ne pas confondre avec l'avis final sur le PC (qui vient après dépôt). Le cadrage est en amont, l'avis PC en aval.

---

## 36. Rapport G2AVP

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport d'étude géotechnique G2 AVP** (Avant-Projet) selon la norme NF P 94-500. Étude réalisée par un bureau d'études géotechnique (Fondasol, Ginger CEBTP, Hydrogéotechnique, Antea, etc.) pour caractériser le sol et fonder le dimensionnement des structures (pieux battus, plots béton, vis ancrées). **Préalable obligatoire au dimensionnement structures** pour permis de construire.

**Format observé** : PDF, 30-80 pages avec annexes (sondages, essais), tableaux et coupes géotechniques.

**Indices internes typiques** :
- **Page de garde** : logo BE géotechnique, titre "Étude géotechnique G2 AVP" ou "Mission G2 Avant-Projet", code projet, commune, date
- **Référence norme** : "NF P 94-500"
- **Sections** : Contexte, Méthodologie (sondages, essais pressiométriques, pénétromètres), Résultats des essais, Caractérisation des sols par horizons (texture, granulométrie, valeurs Em/Pl), Recommandations fondations
- **Annexes** : log de sondages, photos carottes, fiches d'essais, plans d'implantation des sondages
- **Tampon BE + signature ingénieur géotechnicien**

**Nommage probable** : `Rapport_G2AVP_[BE]_[CodeProjet]_[date].pdf`, `Etude_geotechnique_G2AVP_[CodeProjet].pdf`.

**Localisation** : `6 - Techniques/Etude_sol` ou `8-Etude_sol`.

**Piège** : ne pas confondre avec le rapport G2PRO (cf. doc #66 jalon J3) qui est l'étude géotechnique PRO (Projet) plus poussée, attendue en J3. G2 AVP < G2 PRO en niveau de détail.

---

## 37. Rapport étude pédologique / ZH / Faune et Flore / EIE

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Document fusionné** regroupant les rapports environnementaux : étude pédologique, zones humides, inventaires faune et flore, et étude d'impact environnemental (EIE). **Peut être un seul gros rapport ou plusieurs rapports séparés** selon le BE.

**Format observé** : PDF, 100-300+ pages selon ampleur (rapport unique) ou plusieurs PDF (rapports séparés par thématique).

**Indices internes typiques** :
- **Page de garde** : logo BE environnemental (Biotope, Calidris, Egis, Naldéo, etc.) + EnerVivo client + titre "Volet Naturel de l'Étude d'Impact" / "VNEI" / "Étude d'impact écologique" / "Inventaires faune-flore et zones humides"
- **Cadre réglementaire** : références au Code de l'environnement (R. 122-2, L. 411-1, L. 211-1), arrêté du 24 juin 2008 sur les zones humides
- **Sections typiques** :
  - **Pédologie / Zones humides** : sondages pédologiques, classification GEPPA, délimitation des ZH selon critères pédologiques et floristiques
  - **Faune** : inventaires 4 saisons (oiseaux nicheurs/hivernants/migrateurs, mammifères, chiroptères, reptiles, amphibiens, insectes)
  - **Flore et habitats** : relevés phytosociologiques, cartographie des habitats EUNIS/Natura 2000
  - **Évaluation des impacts** : analyse des effets sur les espèces et habitats
  - **Mesures ERC** : Éviter, Réduire, Compenser
- **Annexes** : cartes, fiches espèces, tableaux d'inventaires, méthodologies détaillées
- **Saisons** : mention "Saison 1" / "Saison 2" / "VNEI complet" selon avancement

**Nommage probable** : `Rapport_VNEI_[BE]_[CodeProjet]_S[X]_[date].pdf`, `EIE_complete_[CodeProjet]_[date].pdf`, `Etude_FFH_ZH_[CodeProjet].pdf`.

**Localisation** : `7 - Achat-Fournisseurs/1-Consultations/EIE` ou par BE.

**Pièges à éviter** :
1. **Plusieurs versions saisons** : Saison 1 (printemps/été) puis Saison 2 (automne/hiver) — VNEI complet seulement après les 4 saisons
2. **Drafts vs version finale** : suffixe `_DRAFT` ou `_v1` indique version intermédiaire — chercher la version finale
3. **Documents séparés** : si plusieurs PDF (un par thématique), le LLM doit considérer le doc "présent" dès qu'au moins le rapport VNEI ou EIE final est trouvé

---

## 38. Rapport EPA final

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Livrable final de l'Étude Préalable Agricole** (cf. devis EPA doc #12 commandé en J2a). Rapport complet émis par le BE agricole (Artifex, Naldéo, Agroconsult, etc.) répondant aux exigences du Décret n° 2016-1190 et de l'article L. 112-1-3 du Code rural. **Obligatoire si emprise > seuil départemental** (1-10 ha selon département, défaut 5 ha) en zone agricole.

**Format observé** : PDF, 80-200 pages avec annexes.

**Indices internes typiques** :
- **Page de garde** : logo BE agricole + EnerVivo client + titre "Étude Préalable Agricole" + code projet + commune + département + date
- **Cadre réglementaire** : références Décret 2016-1190, article L. 112-1-3 Code rural, CDPENAF
- **Sections obligatoires** (article D. 112-1-19) :
  1. Description du projet et délimitation du territoire
  2. État initial de l'économie agricole du territoire (production primaire, transformation, commercialisation)
  3. Effets positifs et négatifs sur l'économie agricole + évaluation financière
  4. Mesures d'évitement et de réduction
  5. Mesures de compensation collective (le cas échéant) + coût + modalités
- **Sections type** : Cadre de référence, État initial, Impacts, Mesures ERC, Compensation collective
- **Cartographies** : parcellaire, occupation des sols, sols pédologiques
- **Annexes** : entretiens exploitants, données INSEE/RGA, tableaux statistiques

**Nommage probable** : `Rapport_EPA_[BE]_[CodeProjet]_v[X].pdf`, `Etude_prealable_agricole_[Commune]_[date].pdf`, `EPA_final_[CodeProjet].pdf`.

**Pièges à éviter** :
1. **Drafts vs version finale** : versions intermédiaires (`_v1`, `_DRAFT`, `_provisoire`) à distinguer de la version finale validée
2. **Ne pas confondre avec le devis EPA** (commande en J2a, 20-30 pages) — le rapport EPA fait 80-200+ pages avec contenu d'étude
3. **Cas par cas** : si emprise sous seuil départemental, EPA non requis (N/A)

---

## 39. Étude architecte

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Étude architecturale** obligatoire si la surface de plancher du projet > 150 m² (800 m² pour bâtiments agricoles, 2000 m² pour serres de production sous conditions). Réalisée par un architecte inscrit à l'Ordre des Architectes. Cas par cas pour PV au sol — souvent **N/A** car les centrales PV sol n'ont pas de surface de plancher au sens du Code de l'urbanisme.

**Format observé** : PDF mêlant texte et plans architecturaux.

**Indices internes typiques** :
- **Cartouche architecte** : nom de l'agence d'architecture, numéro d'inscription Ordre des Architectes (NCI), adresse
- **Sections** : Notice descriptive (PC4), insertion paysagère (PC5, PC6), plans (PC2, PC3), perspectives (PC7, PC8)
- **Référence Code de l'urbanisme** : article L. 431-1 (recours obligatoire à un architecte)
- **Signature architecte**

**Nommage probable** : `Etude_architecte_[Agence]_[CodeProjet].pdf`, `Notice_architecturale_[CodeProjet].pdf`.

**Stratégie de classification** : si projet en DP (Déclaration Préalable) au lieu de PC → typiquement pas d'architecte requis → marquer N/A. Si projet en PC avec surface plancher > 150 m² → obligatoire.

---

## 40. Rapport géomètre

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Document du géomètre-expert attestant du bornage et de la délimitation précise des parcelles du projet. Inclut typiquement le plan topographique du site, les niveaux altimétriques, les limites cadastrales reconnues et les éventuels procès-verbaux de bornage avec les propriétaires voisins.

**Format observé** : PDF + DWG (plans techniques), document multi-pages 10-30 pages.

**Indices internes typiques** :
- **Cartouche géomètre** : nom du cabinet de géomètres-experts (souvent inscription OGE — Ordre des Géomètres-Experts), adresse
- **Titre** : "Plan de bornage", "Plan topographique", "PV de bornage contradictoire"
- **Mention** : "Géomètre-Expert", numéro d'inscription OGE
- **Contenu** : Plan topographique avec courbes de niveau, limites parcellaires, bornes posées, table des superficies, références cadastrales
- **Signatures** : géomètre-expert + propriétaires voisins (si bornage contradictoire)

**Nommage probable** : `Plan_bornage_[CodeProjet]_signe.pdf`, `Rapport_geometre_[CodeProjet]_[date].pdf`, `PV_bornage_[Proprio].pdf`.

**Localisation** : `4 - Documents Administratifs/5-Geometre` ou `Geometre`.

**Piège** : distinguer le **plan de bornage** (qui acte les limites) du **simple relevé topographique** (qui mesure le terrain). Pour J2b, le plan de bornage signé contradictoire est le livrable attendu.

---

## 41. Attestation cas par cas validé

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Décision de la DREAL** suite à examen au cas par cas (procédure de demande d'examen au cas par cas / saisine cas par cas), précisant si le projet est soumis à étude d'impact environnementale ou non. Procédure prévue par l'article R. 122-3 du Code de l'environnement.

**Format observé** : PDF officiel préfecture/DREAL, 5-15 pages.

**Indices internes typiques** :
- **En-tête** : République Française + logo DREAL ou Préfecture
- **Titre** : "Décision d'examen au cas par cas" ou "Arrêté préfectoral - examen cas par cas"
- **Référence dossier** : numéro de dossier DREAL, date de saisine
- **Conclusion clé** : "Le projet [n']est [pas] soumis à étude d'impact" — c'est la décision attendue
- **Motivation** : analyse des impacts potentiels sur les milieux, justification de la décision
- **Voies et délais de recours** en fin de document
- **Signature** : Préfet ou Directeur DREAL par délégation

**Nommage probable** : `Decision_cas_par_cas_DREAL_[CodeProjet]_[date].pdf`, `Cas_par_cas_valide_[CodeProjet].pdf`.

**Localisation** : `4 - Documents Administratifs/14-Dossier Cas par Cas` ou équivalent.

**Stratégie de classification** :
1. Si document = **décision DREAL signée avec date de notification** → cas par cas validé (statut Présent)
2. Si seulement la **demande déposée** (pas encore reçue de réponse) → flag Ambigu avec note "Saisine déposée, décision DREAL en attente"
3. Si document = **arrêté soumettant à étude d'impact** → projet soumis à EIE (cas plus lourd)

**Piège** : ne pas confondre **demande** (saisine déposée par EnerVivo) et **décision** (réponse DREAL). Seule la décision validée valide le jalon.

---

## 42. PRAC reçue

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**PRAC = Proposition de Raccordement Avant Complétude de la demande**. Document adressé par Enedis au Demandeur (EnerVivo / SPV), **après paiement d'un devis préalable**, à la suite d'une demande anticipée de raccordement faite par le Demandeur. Reprend les éléments techniques et financiers de la prestation de raccordement ainsi que le délai prévisionnel de mise en exploitation.

Il s'agit d'**un devis qui peut se transformer en Proposition Technique et Financière** (PTF) au sens de la délibération de la **CRE n° 2019-66 du 21 mars 2019** sous certaines conditions. La PRAC est donc une étape précoce dans le processus de raccordement Enedis, antérieure à la PTF définitive (cf. doc #60).

**Format observé** : PDF officiel Enedis, 5-20 pages.

**Indices internes typiques** :
- **En-tête Enedis** : logo Enedis, mention "GRD - Gestionnaire du Réseau de Distribution"
- **Titre** : "Proposition de Raccordement Avant Complétude" ou "PRAC"
- **Référence** : numéro de demande Enedis, date de saisine, mention "demande anticipée"
- **Référence réglementaire** : délibération CRE n° 2019-66 du 21 mars 2019
- **Contenu** : puissance demandée (en kVA), point de raccordement envisagé, longueur ligne à créer, coût estimé, **délai prévisionnel de mise en exploitation**
- **Mention paiement devis préalable** : référence au devis acquitté qui a permis l'émission de la PRAC
- **Mention** : "valable [X] mois", conditions de transformation en PTF

**Nommage probable** : `PRAC_ENEDIS_[CodeProjet]_[date].pdf`, `Proposition_raccordement_avant_completude_[CodeProjet].pdf`.

**Stratégie de classification (PRAC vs PTF)** :
1. Si mention **"Avant Complétude"** ou "demande anticipée" → PRAC (doc #42, J2b)
2. Si mention **"Proposition Technique et Financière" finale** sans référence à l'anticipation → PTF (doc #60, J3)
3. Les deux documents peuvent coexister sur un même projet : PRAC en J2b (étude préliminaire), PTF en J3 (étude définitive post-PC obtenu)

**Piège** : ne pas confondre PRAC avec PTF. La PRAC est antérieure, plus indicative, avec valeurs susceptibles d'évoluer. La PTF est l'engagement ferme d'Enedis.

---

## 43. Arrêté municipal passage des parcelles en ZAENR

- **Jalon** : J2b
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Arrêté municipal** délibérant le passage des parcelles concernées par le projet en **Zone d'Accélération des Énergies Renouvelables** (ZAENR) — dispositif issu de la Loi n° 2023-175 du 10 mars 2023 (article 15). Les ZAENR sont identifiées par les communes pour faciliter l'implantation des projets ENR.

**Format observé** : PDF, arrêté ou délibération municipale, 2-5 pages.

**Indices internes typiques** :
- **En-tête** : Mairie de [Commune], logo, République Française
- **Titre** : "Délibération du Conseil Municipal" ou "Arrêté municipal" + "Zone d'Accélération des Énergies Renouvelables" / "ZAENR"
- **Référence** : numéro de délibération, date du Conseil Municipal
- **Référence loi** : "Loi n° 2023-175 du 10 mars 2023 (...) article L. 141-5-3 du Code de l'énergie"
- **Carte des ZAENR** : périmètres délimités sur le territoire communal
- **Décision** : "DECIDE de classer les parcelles [...] en ZAENR" ou équivalent
- **Signature maire** + tampon de mairie

**Nommage probable** : `Arrete_ZAENR_[Commune]_[date].pdf`, `Deliberation_ZAENR_[Commune]_[CodeProjet].pdf`.

**Piège** : pas tous les projets ont ZAENR (toutes les communes n'en ont pas encore défini). Si la commune n'a pas de ZAENR → marquer N/A.

---

## 44. Récépissé dépôt PC ou DP

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Récépissé officiel** de dépôt du dossier de **Permis de Construire** (PC) ou de **Déclaration Préalable** (DP) en mairie. Document court avec **cachet de la mairie** confirmant la prise en compte du dossier et faisant courir les délais d'instruction.

**Format observé** : PDF scanné, 1-2 pages, formulaire CERFA tamponné.

**Indices internes typiques** :
- **En-tête CERFA** : formulaire CERFA n° 13409*XX (PC) ou n° 13404*XX (DP)
- **Titre** : "Récépissé de dépôt" ou "Accusé de réception d'un dossier de permis de construire"
- **Cachet mairie** : tampon avec nom de la commune + date de dépôt
- **Numéro de dossier** : `PC [INSEE] [Année] [N°]` ou `DP [INSEE] [Année] [N°]`
- **Identification demandeur** : SAS ENERVIVO
- **Identification terrain** : cadastre, surface, adresse
- **Mention** : "Le délai d'instruction est de [X] mois à compter de cette date"

**Nommage observé** : `Recepisse_depot_PC_[date].pdf`, `Recepisse_DP_[CodeProjet]_[date].pdf`, `AR_depot_PC_[CodeProjet].pdf`.

**Localisation** : `4 - Documents Administratifs/7-Urbanisme/PC` ou `DP`.

**Piège** : ne pas confondre avec l'arrêté de PC (qui vient à l'instruction finalisée, en J3). Le récépissé n'est que la **preuve de dépôt**, pas une autorisation.

---

## 45. Projet de bail (notaire)

- **Jalon** : J2b
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Projet de bail emphytéotique rédigé par le notaire, sous forme de **draft pré-signature**. Document préparatoire à la signature du bail définitif (qui interviendra en J3 — cf. doc #58). Permet de valider les termes juridiques avec les parties avant la signature solennelle.

**Format observé** : PDF, 25-40 pages (similaire à la PDB mais en version "bail définitif" et non "promesse").

**Indices internes typiques** :
- **En-tête** : Office Notarial
- **Titre** : "BAIL EMPHYTEOTIQUE" (et non "PROMESSE DE BAIL")
- **Articles** : structurés en Articles 1 à N similaires à la PDB mais avec clauses définitives
- **Durée** : 25-40 ans (bail emphytéotique long, vs 48 mois pour la PDB)
- **Loyers/redevances** : montant définitif en € HT/ha/an
- **Mention "Projet" ou "Draft"** : pour distinguer du bail signé
- **Pas encore de signatures** ou seulement les paraphes notaire

**Nommage probable** : `Projet_bail_[Proprio]_[CodeProjet]_draft.pdf`, `Bail_emphyteotique_projet_[Notaire].pdf`.

**Stratégie de classification** :
1. Si **mention "Projet" et pas de signatures parties** → projet de bail (J2b)
2. Si **signatures des deux parties** + mention "Acte authentique" → bail signé (J3, cf. doc #58)

---

## 46. Plan de masse version J2b

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2b du Plan de masse — mêmes principes que J1/J2a (cf. docs #3, #16). Indices de jalon spécifiques :
- **Cartouche** : `Phase : APD` (Avant-Projet Détaillé) confirmé, ou parfois `EXE` selon convention
- **Indice de révision** : typiquement `Ind C` (ou `Ind B` si nomenclature compacte)
- **Version "dépôt PC/DP"** : c'est le plan de masse joint au dossier de permis de construire ou déclaration préalable
- **Caractéristiques techniques** : données complètes (modèle final, P50/P90 connus, surface précise)

**Nommage observé probable** : `YYMMDD_[CodeProjet]_Plan_Masse_depot_PC.dwg`, `YYMMDD_[CodeProjet]_Plan_Masse_Ind_C.pdf`.

**Stratégie** : si présence de mention "dépôt PC" ou "PC0" dans le nom ou le cartouche → Plan de masse J2b.

---

## 47. TADD version J2b

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2b du TADD — mêmes principes que J1/J2a (cf. docs #4, #17). Spécificités :
- Hypothèses **figées pour le dépôt PC** : modèle de modules définitif, structures choisies, raccordement chiffré (PRAC reçue)
- Numéro de version interne typiquement le plus élevé jusqu'ici (ex : `v6_6` pour DVAUJANY J2B)
- Jalon `J2B` ou `J2b` dans le nom (cf. exemple `250909_TADD_v6_6_DVAUJANY_J2B_JSW.xlsm`)

---

## 48. Dossier de qualification J2b

- **Jalon** : J2b
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J2b du Dossier de qualification — mêmes principes que J1/J2a (cf. docs #5, #32). Contenu spécifique J2b :
- **Jalon `J2b` explicite dans le nom** du fichier (cf. exemple `260305_DVAUJANY_dossier_qualification_J2b_PAP.pptx`)
- Intègre : tous les avis instances (DDT, SDIS, ZAENR), rapports environnementaux (VNEI), géotechnique G2 AVP, bornage géomètre, plan de masse APD, TADD v finale J2b, dossier PC déposé
- Slides typiques additionnelles : "Synthèse études environnementales", "Bilan ICPE/Cas par cas", "Dépôt PC", "Calendrier d'instruction"

---

# J3 — Préparation Ready to Build

## 49. ANRNR

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**ANRNR = Attestation de Non-Recours et de Non-Retrait** délivrée par la mairie après la purge complète des délais de recours contre le permis de construire (ou la déclaration préalable). Document attestant que :
1. Aucun recours contentieux n'a été déposé contre la décision d'urbanisme
2. La décision n'a pas été retirée par l'administration

**Document central pour la sécurité juridique du projet** — sans ANRNR, l'autorisation reste susceptible d'annulation.

**Format observé** : PDF officiel mairie, 1-2 pages.

**Indices internes typiques** :
- **En-tête** : Mairie de [Commune], République Française, logo
- **Titre** : "Attestation de non-recours et de non-retrait" ou "Certificat de non-recours"
- **Référence** : numéro du PC/DP, date de l'arrêté, date d'affichage en mairie, date d'affichage sur le terrain (panneau de chantier)
- **Mention clé** : "atteste qu'aucun recours n'a été enregistré dans les délais légaux de [2 mois pour PC / 1 mois pour DP]"
- **Mention** : "et que la décision n'a pas fait l'objet d'un retrait"
- **Signature maire** + **tampon mairie**

**Nommage probable** : `ANRNR_[CodeProjet]_[date].pdf`, `Attestation_non_recours_[Commune].pdf`, `Certificat_purge_recours_[CodeProjet].pdf`.

**Piège** : l'ANRNR ne peut être délivrée qu'**après expiration des délais de recours** ET **affichage panneau de chantier conforme**. Si absence du panneau d'affichage installé (cf. document supprimé de V10 — photo panneau d'affichage) ou affichage non conforme, l'ANRNR ne peut pas être délivrée.

---

## 50. Avis CDPENAF

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Avis de la Commission Départementale de Préservation des Espaces Naturels, Agricoles et Forestiers** (CDPENAF) — instance consultative obligatoire pour les projets en zone agricole. Examine l'EPA et la compatibilité du projet avec la préservation des terres agricoles. Procédure prévue par les articles L. 112-1-1, L. 112-1-2 du Code rural.

**Format observé** : PDF officiel préfecture, 3-10 pages.

**Indices internes typiques** :
- **En-tête** : République Française, Préfecture de [Dept], DDT
- **Titre** : "Avis de la CDPENAF" ou "Procès-verbal de la CDPENAF"
- **Date de séance** : date de la commission
- **Sections** : Présentation du dossier, Analyse de l'étude préalable agricole, Évaluation des effets, Avis sur les mesures de compensation, **Avis final** (favorable / défavorable / réservé)
- **Position sur la compensation** : montants, modalités, structurations proposées (foncière, financière, mixte)
- **Mention article L. 314-36 Code énergie** si projet agrivoltaïque (loi APER)

**Nommage probable** : `Avis_CDPENAF_[CodeProjet]_[date].pdf`, `PV_CDPENAF_[Dept]_[CodeProjet].pdf`.

**Piège** : l'avis CDPENAF peut être **favorable, défavorable, ou favorable sous conditions**. Si défavorable → blocage projet probable. Vérifier le sens de l'avis (mention explicite en fin de document).

---

## 51-53. PV 1er / 2ème / 3ème passage huissier

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

**Procès-verbaux dressés par un huissier de justice** (officier ministériel devenu commissaire de justice depuis 2022) constatant l'affichage du permis de construire sur le terrain. Trois passages successifs (typiquement à intervalle de 1 mois) pour démontrer la **continuité de l'affichage** pendant les 2 mois de délai de recours.

**Important** : ces PV servent à sécuriser l'ANRNR en démontrant que l'affichage a été ininterrompu, conforme à l'article R. 424-15 du Code de l'urbanisme.

**Format observé** : PDF officiel huissier/commissaire de justice, 3-10 pages par PV.

**Indices internes typiques** :
- **En-tête** : "Étude de Maître [Nom], Commissaire de Justice" (ex-huissier), adresse, mention SCP
- **Titre** : "Procès-verbal de constat" ou "PV de constat d'affichage"
- **Référence** : numéro de PV, date du constat
- **Mention objet** : "constat d'affichage du permis de construire n° [PC...]"
- **Contenu** : description du panneau de chantier (dimensions, contenu, état), localisation GPS, **photos jointes** (panneau visible, lisible, conforme)
- **Mention conformité** : panneau conforme à l'article A. 424-15-1 du Code de l'urbanisme (dimensions 80×120cm, informations obligatoires)
- **Signature huissier + cachet**

**Nommage probable** : `PV_huissier_1er_passage_[CodeProjet]_[date].pdf`, `PV_constat_affichage_2_[CodeProjet].pdf`, etc.

**Stratégie de classification** :
1. Distinguer les **3 PV par ordre chronologique** : le 1er passage typiquement juste après affichage, le 3ème en fin de période de recours
2. Si nom de fichier explicite (`_1er`, `_2eme`, `_3eme`) → classification facile
3. Si nom ambigu → comparer les dates de constat (le plus ancien = 1er passage)

**Piège** : si seul le 1er PV existe sans les autres → flag Ambigu pour vérifier que l'affichage a bien duré 2 mois. Les 3 PV ensemble sont la meilleure preuve.

---

## 54. Présentation de la création SPV à la mairie

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Présentation faite par EnerVivo à la mairie pour annoncer la **création de la Société de Projet (SPV — Special Purpose Vehicle)** dédiée au projet. La SPV est la société qui détiendra le permis, le bail emphytéotique, le contrat d'achat d'électricité et opérera la centrale. Étape de communication politique avec les élus locaux.

**Format observé probable** : `.pptx` ou PDF de présentation, 10-30 slides.

**Indices internes typiques** :
- **Charte EnerVivo** (logo, couleurs vert/jaune)
- **Titre** : "Création de la SPV [Nom projet]" ou "Présentation à la commune de [...]"
- **Slides typiques** :
  - Rappel du projet (puissance, surface, retombées économiques locales)
  - Structure juridique : SPV dédiée, actionnariat (EnerVivo + partenaires éventuels)
  - Identité de la SPV : dénomination, siège, capital, gérance
  - Calendrier : signature bail, construction, MES
  - Engagement local : taxes foncières, IFER, retombées emploi local

**Nommage probable** : `Presentation_SPV_[CodeProjet]_mairie_[date].pptx`, `Creation_SPV_[Nom]_mairie_[Commune].pptx`.

**Piège** : ne pas confondre avec le dossier de qualification (qui est interne VivEpic). Cette présentation est externe (destinée à la mairie).

---

## 55. Kbis SPV

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Extrait Kbis de la **Société de Projet (SPV)** nouvellement créée pour porter le projet PV. Document officiel du RCS attestant l'existence légale de la SPV. Mêmes caractéristiques formelles que le Kbis du propriétaire foncier (cf. doc #21) mais cette fois pour la **société d'exploitation** créée par EnerVivo.

**Format et indices** : identiques au doc #21.

**Spécificité SPV** :
- Dénomination typique : "Centrale [Nom projet]" ou "[Code projet] Énergies" ou "SAS [Nom commune]"
- Forme juridique : SAS (Société par Actions Simplifiée) le plus souvent
- **Capital social** : variable (souvent 1000€ à 10000€ pour SPV ENR)
- **Siège social** : adresse EnerVivo (Bordeaux) ou parfois adresse projet
- **Objet social** : "Production et vente d'électricité d'origine photovoltaïque"
- **Présidence/Gérance** : EnerVivo représenté par Sylvain FREDERIC ou habilité

**Nommage probable** : `Kbis_SPV_[CodeProjet]_[date].pdf`, `Kbis_Centrale_[Nom]_[date].pdf`.

**Piège** : à distinguer du Kbis du propriétaire foncier (doc #21). Le Kbis SPV est récent (postérieur à la création de la SPV en J3).

---

## 56. Statuts SPV signés

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Statuts signés de la **Société de Projet (SPV)** créée par EnerVivo pour porter le projet. Document juridique fondateur de la SPV. Mêmes caractéristiques formelles que les statuts du propriétaire (cf. doc #20) mais pour la SPV d'exploitation.

**Format et indices** : identiques au doc #20.

**Spécificités SPV** :
- **Objet social** typique : "L'étude, la conception, le développement, le financement, la construction, l'exploitation, la maintenance, l'achat et la vente d'électricité d'origine photovoltaïque"
- **Capital social** souvent modeste à la création (1000€ à 10000€), avec possibilité d'augmentation post-closing
- **Présidence / Direction** : EnerVivo (en tant que personne morale) ou Sylvain FREDERIC (en tant que personne physique)
- **Signatures** : EnerVivo représentée par son habilité

**Nommage probable** : `Statuts_SPV_[CodeProjet]_signes.pdf`, `Statuts_Centrale_[Nom]_signes_[date].pdf`.

**Piège** : à distinguer des statuts du propriétaire foncier (doc #20). Les statuts SPV sont récents (postérieurs à la création de la SPV).

---

## 57. Pacte d'actionnaires signé

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Pacte d'actionnaires signé entre les associés de la SPV régissant leurs relations : gouvernance, sortie, préemption, droit de suite, distribution de dividendes, etc. Document complémentaire aux statuts mais avec des clauses confidentielles (alors que les statuts sont publics au RCS).

**Format observé** : PDF, 20-50 pages, document juridique dense.

**Indices internes typiques** :
- **Titre** : "Pacte d'actionnaires" ou "Pacte d'associés" ou "Shareholders Agreement"
- **Identification des parties** : les associés de la SPV (EnerVivo + partenaires éventuels : fonds d'investissement, agriculteur, communauté de communes, etc.)
- **Sections typiques** : Objet, Gouvernance (composition CA, comité de direction), Décisions importantes (majorité qualifiée), Droits de cession (préemption, retrait, exclusion), Garanties, Sortie (rachat, vente, IPO), Confidentialité, Durée
- **Signatures de tous les associés** en fin de document

**Nommage probable** : `Pacte_actionnaires_SPV_[CodeProjet]_signe.pdf`, `Shareholders_Agreement_[CodeProjet]_signed.pdf`.

**Piège** : document **confidentiel** — ne pas exposer son contenu dans les rapports d'audit. Marquer Présent sans détailler les clauses.

---

## 58. Bail signé (acte notarié)

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Bail emphytéotique définitif signé par acte notarié** entre le Promettant (propriétaire foncier) et le Bénéficiaire (devenu la SPV via substitution autorisée par la PDB). **Convertit la PDB en bail emphytéotique authentique** d'une durée typique de 25-40 ans (cf. Annexe 4 de la PDB).

**Format observé** : PDF, 30-50 pages, **acte notarié authentique**.

**Indices internes typiques** :
- **En-tête** : Office Notarial, "Maître [Nom], Notaire"
- **Titre** : "BAIL EMPHYTEOTIQUE" (et non "PROMESSE DE BAIL")
- **Mention** : "Acte authentique" ou "Acte reçu par Maître [...]"
- **Parties** : Bailleur (Promettant) + Emphytéote (SPV après substitution)
- **Articles** : structurés conformément à l'Annexe 4 de la PDB (Destination, Durée, Loyer, Servitudes, Résiliation, Démantèlement)
- **Durée** : 25 ans typiquement (max 99 ans selon Code rural L. 451-1)
- **Loyer** : montant définitif en €/ha/an (typiquement 4500 €/ha/an pour AgriPV)
- **Signatures** : Bailleur + Emphytéote + Notaire (signature électronique ou manuscrite)
- **Publication** : mention de publication au Service de la Publicité Foncière

**Nommage probable** : `Bail_emphyteotique_signe_[CodeProjet]_[date].pdf`, `Acte_authentique_bail_[Commune]_[date].pdf`.

**Pièges** :
1. **Drafts à ignorer** : seul le bail avec signatures notariales et mention "acte authentique" valide le jalon
2. **Distinguer de la PDB** : la PDB est l'engagement préalable (J1), le bail signé est l'acte final (J3)
3. **Substitution** : vérifier que l'Emphytéote est bien la SPV (et non EnerVivo en direct), conformément à la clause de substitution de la PDB

---

## 59. Récépissé de la demande de raccordement / CRD

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

Récépissé/accusé de réception de la **demande de raccordement** déposée par la SPV auprès d'Enedis pour officialiser la connexion au réseau électrique de la centrale. CRD = "Convention de Raccordement et de Distribution" ou "Contrat de Raccordement et de Distribution" selon contexte.

**Format observé** : PDF Enedis, 1-3 pages.

**Indices internes typiques** :
- **En-tête Enedis** : logo, mention GRD
- **Titre** : "Accusé de réception" ou "Récépissé de demande de raccordement"
- **Référence dossier** : numéro Enedis (10 chiffres typiquement)
- **Mention** : "Votre demande de raccordement a été enregistrée"
- **Puissance demandée** : en kVA
- **Identification demandeur** : SPV (et non EnerVivo)
- **Date de dépôt**

**Nommage probable** : `Recepisse_raccordement_ENEDIS_[CodeProjet]_[date].pdf`, `AR_demande_raccordement_[SPV].pdf`.

---

## 60. PTF / CRD reçue d'ENEDIS

- **Jalon** : J3
- **Propriété** : Facultatif
- **Versioning** : Document unique

### Description

**PTF = Proposition Technique et Financière** émise par Enedis pour le raccordement de la centrale au réseau. Document officiel détaillant les modalités techniques (point de raccordement, ligne à créer, postes de transformation) et le **coût du raccordement** (à la charge du producteur).

**Format observé** : PDF Enedis officiel, 20-50 pages avec schémas.

**Indices internes typiques** :
- **En-tête Enedis** : logo, mention GRD
- **Titre** : "Proposition Technique et Financière" ou "PTF"
- **Référence** : numéro PTF, date d'émission
- **Sections** : Caractéristiques du raccordement (puissance, point de livraison, schéma), Travaux côté Enedis, Travaux côté producteur, Coût total HT, Délais de validité (typiquement 3-6 mois)
- **Schémas** : plan de raccordement, schéma unifilaire
- **Conditions de réalisation** : étapes, prérequis, jalons

**Nommage probable** : `PTF_ENEDIS_[CodeProjet]_[date].pdf`, `Proposition_raccordement_[SPV]_[date].pdf`.

---

## 61. PTF / CRD signée

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**PTF/CRD signée** par la SPV (acceptation par la SPV de la proposition Enedis et engagement à payer les travaux de raccordement). **Engagement contractuel ferme** entre la SPV et Enedis.

**Format et indices** : identiques au doc #60 (PTF reçue), mais avec :
- **Signature SPV** sur la PTF (bon pour accord, lu et approuvé)
- **Mention de retour signé** : "Acceptation par le client"
- **Versement d'acompte** : confirmation du versement de l'acompte demandé (souvent 30% du montant total)

**Nommage probable** : `PTF_ENEDIS_[CodeProjet]_signee.pdf`, `PTF_signed_[CodeProjet].pdf`.

**Piège** : drafts à ignorer — seule la version signée et retournée à Enedis valide le jalon.

---

## 62. CRD transférée VivEpic vers SPV

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Document acte le **transfert de la Convention/Contrat de Raccordement et Distribution** (CRD) de **VivEpic vers la SPV** créée pour le projet. Étape administrative pour que la SPV devienne titulaire du raccordement Enedis (au lieu de VivEpic qui avait peut-être initialement déposé la demande).

**Format observé probable** : PDF, document Enedis ou avenant à la PTF, 2-5 pages.

**Indices internes typiques** :
- **En-tête Enedis** ou **VivEpic** selon émetteur
- **Titre** : "Transfert de Convention de Raccordement" ou "Avenant - Changement de titulaire CRD"
- **Ancien titulaire** : VivEpic
- **Nouveau titulaire** : SPV [Code projet]
- **Signature des deux parties** + Enedis

**Nommage probable** : `Transfert_CRD_VivEpic_SPV_[CodeProjet].pdf`, `Avenant_changement_titulaire_[CodeProjet].pdf`.

**Piège** : document spécifique à la procédure interne VivEpic-EnerVivo. Pas systématique (cas par cas).

---

## 63. Consultations / Devis auprès des fournisseurs

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Ensemble des **consultations et devis** reçus des fournisseurs et sous-traitants potentiels pour la construction : EPC (Engineering Procurement Construction), fournitures (modules PV, onduleurs, structures, transformateurs), génie civil, raccordement HTA, etc. Documents préparatoires au montage économique J4.

**Format observé** : multiples PDF (un par devis), parfois rangés dans dossier `7-Achat-Fournisseurs/1-Consultations`.

**Indices internes typiques** :
- Devis émis par fournisseurs : SUNGROW, SMA, HUAWEI (onduleurs), Jinko Solar, JA Solar, LONGi, Trina Solar (modules), Schneider Electric, ABB, Siemens (transformateurs), entreprises de génie civil locales
- Format devis standard : référence, date, validité, prestations, prix HT/TTC, conditions de paiement, signature commercial fournisseur

**Nommage probable** : `Devis_[Fournisseur]_[CodeProjet]_[date].pdf`, `Consultation_[Theme]_[Fournisseur].pdf`.

**Localisation** : `7 - Achat-Fournisseurs/1-Consultations/`.

**Piège** : document **multi-fichiers** par nature — le LLM doit considérer "Présent" dès qu'au moins 1-2 devis sont trouvés. Pas besoin d'avoir l'intégralité des consultations.

---

## 64. CETI

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**CETI = Certificat d'Éligibilité du Terrain d'Implantation**. Certificat délivré par **le préfet de région**, attestant de l'éligibilité d'un terrain pour l'implantation d'une centrale photovoltaïque, dans le cadre des **appels d'offres CRE**.

**Objectif** : minimiser l'impact environnemental et protéger les zones agricoles et boisées, en évaluant le site selon des critères spécifiques fixés par le cahier des charges de chaque appel d'offres. Les projets sont notés en fonction de leur localisation : zones urbanisées ou à urbaniser, zones naturelles hors milieux humides, ou **sites dégradés** (ces derniers obtenant la note maximale pour favoriser la réhabilitation).

**Caractère obligatoire** : ce certificat est **obligatoire pour candidater aux appels d'offres CRE** portant sur des installations au sol de **plus de 500 kWc**, y compris les projets agrivoltaïques où la production agricole reste prioritaire.

**Format observé** : PDF officiel préfecture de région, 3-10 pages.

**Indices internes typiques** :
- **En-tête** : République Française, Préfecture de Région [Nom], logo
- **Titre** : "Certificat d'Éligibilité du Terrain d'Implantation" ou "CETI"
- **Référence dossier** : numéro CETI, date d'émission
- **Identification du projet** : SAS EnerVivo / SPV, code projet, commune, parcelles cadastrales, surface
- **Caractéristiques** : puissance prévisionnelle (> 500 kWc), type de terrain (agricole, dégradé, naturel)
- **Décision préfectorale** : éligibilité confirmée avec **catégorisation du terrain** (zones urbanisées / sites dégradés / zones agricoles / etc.)
- **Notation** : note attribuée selon la grille du cahier des charges de l'AO CRE concerné
- **Référence AO CRE** : période de candidature visée (ex : PPE2 période X)
- **Signature** : Préfet de région ou Directeur DREAL par délégation

**Nommage probable** : `CETI_[CodeProjet]_[date].pdf`, `Certificat_eligibilite_terrain_[CodeProjet].pdf`.

**Lien fonctionnel avec doc #65 (Candidature tarif d'achat)** : la CETI est une pièce justificative obligatoire du dossier de candidature aux AO CRE pour les projets > 500 kWc. Les deux documents vont ensemble.

**Stratégie de classification** :
1. Si projet < 500 kWc OU projet ne candidatant pas à un AO CRE → CETI N/A
2. Si projet > 500 kWc avec candidature AO CRE → CETI obligatoire, à chercher activement
3. Si demande déposée mais certificat non encore reçu → flag Ambigu avec note "Demande CETI déposée, en attente de retour préfecture"

**Piège** : ne pas confondre avec l'attestation de cas par cas (doc #41, J2b) qui concerne l'étude d'impact environnementale. La CETI concerne l'éligibilité du terrain pour les AO CRE.

---

## 65. Candidature tarif d'achat (AO CRE, AOS, S21, ACC)

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Dossier de candidature pour bénéficier d'un **tarif d'achat de l'électricité** via un appel d'offres ou un guichet ouvert :
- **AO CRE** : Appel d'Offres de la Commission de Régulation de l'Énergie (procédure pluri-annuelle pour grands projets)
- **AOS** : Appel d'Offres Simplifié
- **S21** : guichet ouvert tarif S21 (centrales sol < 500 kWc, anciennement)
- **ACC** : guichet AutoConsommation Collective ou Achat Court-circuit (selon contexte)

**Format observé** : dossier multi-documents PDF + formulaires, plusieurs dizaines de pages.

**Indices internes typiques** :
- **Référence CRE** : numéro de période d'AO, famille tarifaire (T1, T2, T3, T4 selon puissance et terrain)
- **Cahier des charges** : document de référence CRE
- **Pièces du dossier** : note descriptive, plan d'implantation, justificatifs (PC déposé, foncier sécurisé), engagement de prix de vente proposé (€/MWh)
- **Mention** : "Candidature à l'appel d'offres CRE n° [...]" ou "Demande de contrat d'achat S21"
- **Bordereau de prix** : prix de vente proposé en €/MWh

**Nommage probable** : `Candidature_AO_CRE_PPE2_[CodeProjet].pdf`, `Dossier_S21_[CodeProjet].pdf`, `Candidature_AOS_[CodeProjet].pdf`.

**Localisation** : dossier dédié `Appels_offres` ou `Candidatures_CRE`.

**Piège** : selon la taille et le type de projet, certains tarifs ne s'appliquent pas (un projet 7 MWc ne candidatera pas à S21 qui était plafonné à 500 kWc). Vérifier la cohérence puissance / appel d'offres.

---

## 66. Rapport G2PRO

- **Jalon** : J3
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Rapport d'étude géotechnique G2 PRO** (Projet) selon la norme NF P 94-500 — version plus poussée que la G2 AVP (cf. doc #36). Réalisée typiquement **après obtention du PC et avant lancement construction** pour affiner le dimensionnement des fondations. Sondages complémentaires ciblés sur les zones critiques.

**Format et indices** : similaire au doc #36 (G2 AVP), avec différences :
- **Titre** : "Étude géotechnique G2 PRO" ou "Mission G2 Projet"
- **Référence norme** : "NF P 94-500 - Phase G2 PRO"
- **Niveau de détail accru** : plus de sondages, calculs de dimensionnement fondations détaillés (descente de charge par pieu/plot, profondeur d'ancrage, capacité portante)
- **Recommandations** : type de fondation final retenu (pieux battus, vis ancrées, plots béton), profondeur, espacement

**Nommage probable** : `Rapport_G2PRO_[BE]_[CodeProjet].pdf`, `Etude_geotechnique_G2PRO_[CodeProjet].pdf`.

**Piège** : à distinguer absolument de la G2 AVP (doc #36, J2b). G2 PRO arrive en J3, plus détaillée.

---

## 67. Plan de masse version J3

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J3 du Plan de masse — mêmes principes que précédents (cf. docs #3, #16, #46). Spécificités J3 :
- **Cartouche** : `Phase : EXE` (Exécution) ou `PRO` (Projet)
- **Indice de révision** : typiquement `Ind D` (suite logique APS → APD → PRO/EXE)
- **Version "Pré-Ready to Build"** : intègre les retours de la G2 PRO, l'implantation définitive des fondations
- Données techniques affinées : positionnement exact des onduleurs, postes de transformation, postes de livraison

---

## 68. TADD version J3

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J3 du TADD — mêmes principes que précédents (cf. docs #4, #17, #47). Spécificités :
- Hypothèses **finalisées pour le closing bancaire** à venir (J4)
- Intègre : PTF Enedis signée, devis EPC consolidés, tarif d'achat retenu (post-candidature CRE)
- TRI / VAN définitifs pour validation comité d'investissement

---

## 69. Dossier de qualification J3

- **Jalon** : J3
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J3 du Dossier de qualification — mêmes principes que précédents (cf. docs #5, #32, #48). Contenu spécifique J3 :
- **Jalon `J3` explicite dans le nom**
- Intègre : ANRNR obtenue, avis CDPENAF, PV huissiers, création SPV (Kbis, statuts, pacte), bail signé, raccordement Enedis (PTF signée), G2 PRO, candidature tarif d'achat
- Slides typiques additionnelles : "Sécurité juridique acquise", "SPV constituée", "Bail authentique signé", "Raccordement confirmé", "Synthèse tarif d'achat"

---

# J4 — Montage économique

## 70. Contrat d'achat d'électricité signé

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Contrat d'achat d'électricité** signé entre la SPV (vendeur) et un acheteur (EDF OA pour les tarifs d'achat réglementés, ou un agrégateur/fournisseur privé pour les contrats de gré à gré / PPA). Définit les conditions de vente de l'électricité produite : prix (€/MWh), durée (15-20 ans), modalités de paiement, garanties.

**Format observé** : PDF, 30-80 pages, contrat juridique dense.

**Indices internes typiques** :
- **Cas 1 - Tarif d'achat EDF OA** :
  - **Émetteur** : EDF Obligation d'Achat (EDF OA)
  - **Titre** : "Contrat d'achat d'électricité" ou "Contrat d'obligation d'achat" + référence du tarif (S21, T4, etc.) ou de l'appel d'offres (CRE PPE2 période X)
  - **Prix** : tarif fixe en €/MWh sur la durée (typiquement 15 ou 20 ans)
- **Cas 2 - PPA (Power Purchase Agreement)** :
  - **Émetteur** : agrégateur (Engie, Photosol, BayWa r.e., etc.) ou corporate buyer
  - **Titre** : "Power Purchase Agreement" ou "Contrat de gré à gré"
  - **Prix** : variable ou fixe selon négociation
- **Signatures** : SPV (par EnerVivo) + Acheteur

**Nommage probable** : `Contrat_achat_electricite_EDF_OA_[CodeProjet]_signe.pdf`, `PPA_[Acheteur]_[CodeProjet]_signed.pdf`.

**Piège** : drafts à ignorer — seule la version signée des deux parties valide le jalon.

---

## 71. Contrat d'agrégation signé

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

Contrat d'agrégation signé entre la SPV et un **agrégateur d'énergie** (acteur intermédiaire entre producteur et marché spot). Pour les projets bénéficiant du **complément de rémunération** (au lieu du tarif fixe), l'agrégateur assure la vente sur le marché et le calcul du complément. Obligatoire pour les projets en complément de rémunération (typiquement post-CRE).

**Format observé** : PDF, 20-50 pages, contrat type d'agrégateur.

**Indices internes typiques** :
- **Émetteur** : agrégateur (Engie, BayWa r.e., Statkraft, etc.)
- **Titre** : "Contrat d'agrégation" ou "Convention d'agrégation"
- **Sections** : Objet, Durée (souvent alignée sur le contrat d'achat 15-20 ans), Rémunération de l'agrégateur (commission % ou €/MWh), Obligations de prévision et d'équilibrage, Garanties
- **Signatures** : SPV + agrégateur

**Nommage probable** : `Contrat_agregation_[Agregateur]_[CodeProjet]_signe.pdf`.

**Piège** : cas par cas — pas obligatoire pour tous les projets (uniquement pour ceux en complément de rémunération).

---

## 72. Offre bancaire signée

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Term sheet / lettre d'offre indicative** signée entre la SPV et la banque finançante (Term Sheet validée), précisant les conditions principales du financement du projet : montant, durée, taux, garanties, ratios financiers (DSCR, gearing). Préalable au **Closing Bancaire** (doc #73).

**Format observé** : PDF, 10-30 pages.

**Indices internes typiques** :
- **Émetteur** : banque (BPCE Énergies Vertes, Crédit Agricole CIB, Banque Postale, BNP Paribas, BPI France, etc.)
- **Titre** : "Term Sheet" ou "Offre de financement" ou "Lettre d'engagement"
- **Sections** : Montant du financement (€), Durée (typiquement 15-18 ans en project finance), Taux (fixe ou variable indexé sur Euribor + marge), Ratios financiers (DSCR > 1,20 typiquement), Garanties (nantissement actions SPV, cession PPA, cession CRD, etc.)
- **Signature** : SPV + banque

**Nommage probable** : `Term_sheet_[Banque]_[CodeProjet]_signe.pdf`, `Offre_bancaire_[Banque]_signed.pdf`.

---

## 73. Closing Bancaire / Documents de crédit signés

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Documents de closing bancaire** : ensemble des contrats de financement signés finalisant le tour de table financier (Senior Loan Agreement, sûretés, garanties). Étape majeure : déblocage du financement de la construction.

**Format observé** : multiples PDF (10+ documents par closing), document type **Senior Facility Agreement** (50-150 pages).

**Indices internes typiques** :
- **Documents typiques du closing** :
  - **Senior Loan Agreement** ou "Contrat de prêt senior"
  - **Pacte d'actionnaires révisé** (avec banque éventuellement)
  - **Conventions de subordination**
  - **Actes de nantissement** : actions SPV, comptes bancaires SPV, créances futures (PPA, CRD)
  - **Conventions de gestion** des comptes (DSRA, Operating account)
  - **Garanties à première demande** des sponsors
  - **Sûretés sur le bail emphytéotique**
- **Mention "Effective Date" ou "Date de mise à disposition"** : date à partir de laquelle les fonds sont disponibles
- **Signatures** : SPV + banque(s) + sponsors (EnerVivo) + souvent notaire pour les actes notariés

**Nommage probable** : `Closing_bancaire_[CodeProjet]_[date].pdf`, `Senior_Loan_Agreement_[CodeProjet]_signed.pdf`, dossier `Closing_[CodeProjet]_[date]/`.

**Piège** : closing = ensemble de documents (pas un seul). Le LLM doit accepter "Présent" dès que les principaux documents (Senior Loan Agreement + actes de nantissement) sont trouvés.

---

## 74. Contrat EPC signé

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

**Contrat EPC = Engineering Procurement Construction** signé entre la SPV et l'entreprise de construction (EPC contractor). Contrat clé en main pour la conception, l'approvisionnement et la construction de la centrale. Cas par cas car certains projets sont en multi-lots (pas d'EPC global).

**Format observé** : PDF, 50-150 pages avec annexes techniques.

**Indices internes typiques** :
- **Émetteur / EPC contractor** : entreprise type Eiffage Énergies, Spie Industries, Equans, Bouygues Énergies, EDF Renouvelables, Photosol, BayWa, ou intégrateur local
- **Titre** : "Contrat EPC" ou "Contrat clé en main" ou "Engineering Procurement Construction Agreement"
- **Sections** : Objet (centrale [X] MWc clé en main), Prix forfaitaire (€ HT), Délais de livraison (date COD = Commercial Operation Date), Garanties techniques (performance, productible), Pénalités de retard, Maintenance pendant la garantie
- **Annexes techniques** : spécifications modules, onduleurs, structures, schéma unifilaire, plan de masse
- **Signatures** : SPV + EPC contractor

**Nommage probable** : `Contrat_EPC_[Entreprise]_[CodeProjet]_signe.pdf`, `EPC_Agreement_signed_[CodeProjet].pdf`.

---

## 75. Contrat AMO signé

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Version signée uniquement

### Description

**Contrat AMO = Assistance à Maîtrise d'Ouvrage** signé entre la SPV et un AMO indépendant. L'AMO accompagne le maître d'ouvrage (la SPV) dans la supervision technique du chantier, le contrôle qualité, le suivi des essais et la réception. Indépendant de l'EPC pour garantir la qualité.

**Format observé** : PDF, 20-40 pages.

**Indices internes typiques** :
- **AMO type** : bureau d'études indépendant (BEPV, Solarama, Sereo, etc.)
- **Titre** : "Contrat d'Assistance à Maîtrise d'Ouvrage" ou "AMO Contract"
- **Sections** : Missions (validation conception, suivi chantier, OPC, réception, levée des réserves), Honoraires (forfait ou taux journalier), Durée (de la signature à la fin de garantie de parfait achèvement)
- **Signatures** : SPV + AMO

**Nommage probable** : `Contrat_AMO_[Entreprise]_[CodeProjet]_signe.pdf`.

---

## 76. Devis génie civil signé

- **Jalon** : J4
- **Propriété** : Facultatif
- **Versioning** : Version signée uniquement

### Description

Devis signé pour les **travaux de génie civil** (terrassements, fondations, voiries, clôtures, locaux techniques). Si projet en multi-lots (pas d'EPC global), le génie civil est contracté séparément.

**Format observé** : PDF devis classique signé.

**Indices internes typiques** :
- **Émetteur** : entreprise de génie civil locale ou nationale (TPSO, Eiffage Génie Civil, Razel, Colas, etc.)
- **Titre** : "Devis génie civil" + référence projet
- **Prestations** : terrassement, voiries, plates-formes locaux techniques, clôtures, portails, citerne SDIS, etc.
- **Signature** : entreprise + SPV (bon pour accord)

**Nommage probable** : `Devis_GC_[Entreprise]_[CodeProjet]_signe.pdf`.

---

## 77. Devis installation centrale PV signé

- **Jalon** : J4
- **Propriété** : Facultatif
- **Versioning** : Version signée uniquement

### Description

Devis signé pour l'**installation de la centrale PV** : fourniture et pose des structures, modules, onduleurs, câbles, transformateurs, postes de livraison. Si projet en multi-lots, contrat séparé du génie civil.

**Format et indices** : similaires au doc #76, avec spécificité PV (modules Jinko/JA/LONGi, onduleurs SMA/SUNGROW, structures TrinaTracker/Soltigua/Schletter, etc.).

**Nommage probable** : `Devis_installation_PV_[Entreprise]_[CodeProjet]_signe.pdf`.

---

## 78. Contrat O&M signé

- **Jalon** : J4
- **Propriété** : Facultatif
- **Versioning** : Version signée uniquement

### Description

**Contrat O&M = Operation & Maintenance** signé entre la SPV et un prestataire de maintenance. Couvre l'exploitation et la maintenance de la centrale pendant son exploitation (20-30 ans). Souvent signé en J4 (avant construction) pour démarrage post-MES.

**Format observé** : PDF, 30-60 pages.

**Indices internes typiques** :
- **Émetteur O&M** : prestataire spécialisé (Solarama O&M, BayWa r.e. Operations, Engie Solutions, BlueSky, Idex, Photosol Asset Management, etc.)
- **Titre** : "Contrat O&M" ou "Operation & Maintenance Agreement"
- **Sections** : Périmètre (maintenance préventive + curative + monitoring + reporting), Durée (5-10 ans renouvelable), Rémunération (forfait €/MWc/an ou €/MWh), KPI (disponibilité minimale, PR — Performance Ratio), Garanties
- **Signatures** : SPV + O&M provider

**Nommage probable** : `Contrat_OM_[Prestataire]_[CodeProjet]_signe.pdf`, `OM_Agreement_signed_[CodeProjet].pdf`.

---

## 79. CARDi

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**CARDi = Contrat d'Accès au Réseau de Distribution pour l'injection** — contrat tripartite (ou bipartite avec Enedis) régissant l'accès de la SPV au réseau Enedis pour l'injection de l'électricité produite. Distinct de la PTF (qui concerne le raccordement physique).

**Format observé probable** : PDF, 20-50 pages, contrat type Enedis.

**Indices internes typiques** :
- **Émetteur** : Enedis
- **Titre** : "Contrat d'Accès au Réseau de Distribution pour l'Injection" ou "CARDi"
- **Référence Enedis** : numéro de contrat
- **Sections** : Objet (accès réseau), Tarif d'utilisation (TURPE), Comptage, Mise à disposition, Responsabilité d'équilibre
- **Signatures** : SPV + Enedis

**Nommage probable** : `CARDi_ENEDIS_[CodeProjet]_signe.pdf`, `Contrat_acces_reseau_[CodeProjet].pdf`.

---

## 80. Assurance RC Pro souscrite

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Attestation d'assurance Responsabilité Civile Professionnelle** souscrite par la SPV. Couvre la responsabilité de la SPV vis-à-vis des tiers pendant l'exploitation de la centrale.

**Format observé** : PDF attestation assureur, 1-2 pages.

**Indices internes typiques** :
- **En-tête assureur** : logo (Allianz, AXA, Generali, Groupama, Crédit Agricole Assurances, etc.)
- **Titre** : "Attestation d'assurance RC Professionnelle"
- **Identification souscripteur** : SPV [Nom projet]
- **Garanties** : montants par sinistre, plafond annuel, franchises
- **Période de validité** : date début + date fin
- **Signature assureur** ou cachet

**Nommage probable** : `Attestation_RC_Pro_[Assureur]_[SPV].pdf`.

---

## 81. Assurance Dommage-Ouvrage (DO)

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Attestation d'assurance **Dommage-Ouvrage** souscrite par la SPV (maître d'ouvrage). Couvre les dommages affectant la solidité de l'ouvrage pendant 10 ans (garantie décennale). Obligatoire pour les constructions au sens de la loi Spinetta (1978).

**Format et indices** : similaires au doc #80, avec spécificités DO (référence article L. 242-1 Code des assurances, garantie décennale Spinetta).

**Nommage probable** : `Attestation_DO_[Assureur]_[CodeProjet].pdf`.

**Piège** : pour les centrales PV au sol, l'application du DO est parfois discutée juridiquement (selon que le PV est qualifié de "construction" ou "équipement"). Vérifier.

---

## 82. Assurances décennales prestataires

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Attestations d'**assurance décennale** des prestataires intervenant sur le chantier (EPC contractor, génie civil, installateurs PV, électriciens). Chaque entreprise du BTP doit fournir son attestation décennale couvrant ses interventions.

**Format observé** : multiples PDF (un par prestataire), attestations assureurs.

**Indices internes typiques** :
- **Émetteur** : assureur de chaque prestataire (SMA BTP, MAAF Assurances, GAN, etc.)
- **Titre** : "Attestation d'assurance décennale" ou "Attestation garantie décennale"
- **Identification prestataire** : raison sociale, SIRET, activités assurées (gros œuvre, second œuvre, lots techniques)
- **Période de validité** : année en cours
- **Référence article 1792 du Code civil**

**Nommage probable** : `Decennale_[Prestataire]_[Annee].pdf`.

**Stratégie** : LLM marque "Présent" si attestations des principaux prestataires (EPC, GC, électricien) sont trouvées. Pas besoin d'avoir l'intégralité des sous-traitants.

---

## 83. Dossier EXE

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Dossier EXE = Dossier d'Exécution** — ensemble des plans et notes techniques d'exécution permettant la construction effective de la centrale. Élaboré par le bureau d'études techniques (ou l'EPC contractor) à partir des études PRO. Validé avant lancement du chantier.

**Format observé** : multiples fichiers (plans DWG, PDF, notes de calcul, schémas), organisés par lot.

**Indices internes typiques** :
- **Titre** : "Dossier d'Exécution" ou "EXE" ou "Documents d'exécution"
- **Contenu typique** :
  - Plans d'exécution structures (implantation tables, fondations)
  - Plans d'exécution électriques (cheminements câbles, schéma unifilaire détaillé, plan de mise à la terre)
  - Notes de calcul (descente de charges, dimensionnement fondations, vérification mécanique structures)
  - Plans VRD (voiries, réseaux divers)
  - Schémas postes de livraison et de transformation
  - Plans d'exécution clôtures, accès, citerne SDIS
- **Cartouches** : Phase EXE / Ind A, B, C selon révisions
- **Validation** : VISA du bureau de contrôle (Apave, Veritas, Socotec)

**Nommage probable** : dossier `Dossier_EXE_[CodeProjet]/` contenant multiples PDF/DWG.

**Piège** : document **multi-fichiers**. LLM marque "Présent" si au moins le sommaire EXE et quelques plans clés sont trouvés.

---

## 84. Pull out test

- **Jalon** : J4
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Pull-out test = essai d'arrachement** réalisé sur le terrain pour vérifier la capacité d'ancrage des structures (pieux battus principalement). Test mécanique destructif sur quelques pieux témoins, comparant la résistance mesurée à la résistance calculée. **Préalable au lancement de la fondation en masse**.

**Format observé** : PDF rapport d'essai, 10-30 pages.

**Indices internes typiques** :
- **Émetteur** : bureau d'études géotechnique (Fondasol, CEBTP, Antea, etc.) ou laboratoire spécialisé
- **Titre** : "Rapport d'essais de chargement" ou "Pull-out tests" ou "Essais d'arrachement"
- **Méthodologie** : nombre de pieux testés (typiquement 3-5), profondeur d'enfoncement, charge appliquée par paliers
- **Résultats** : courbes charge/déplacement, valeur de charge limite mesurée
- **Comparaison aux valeurs de calcul** : conformité ou nécessité d'adapter le dimensionnement
- **Photos** : équipement d'essai sur le terrain

**Nommage probable** : `Pull_out_test_[CodeProjet]_[date].pdf`, `Essais_arrachement_pieux_[CodeProjet].pdf`.

---

## 85. Plan de masse version J4

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J4 du Plan de masse — version **"finale pour construction"**, intégrant les ajustements post-pull-out test et toutes les validations bureau de contrôle. Indices :
- **Cartouche** : `Phase : EXE` (Exécution) confirmé
- **Indice de révision** : typiquement `Ind E` ou plus (révisions multiples accumulées)
- **Validation** : VISA bureau de contrôle dans cartouche
- **Statut** : "BPE" (Bon Pour Exécution) ou "DEX" (Document EXécution)

---

## 86. TADD version J4

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J4 du TADD — version **post-closing bancaire**, avec toutes les hypothèses figées et financements bouclés. Spécificités :
- Intègre : closing bancaire (taux de prêt final, échéanciers), contrats EPC/O&M signés (CAPEX/OPEX définitifs), contrat d'achat signé (revenus garantis)
- **Plan d'affaires définitif** pour la SPV — base du suivi exploitation à partir de la MES
- Jalon `J4` dans le nom

---

## 87. Dossier de qualification J4

- **Jalon** : J4
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

Version J4 du Dossier de qualification — **dernier dossier de qualification avant construction**. Contenu :
- **Jalon `J4` explicite dans le nom**
- Intègre : tous les contrats signés (achat électricité, agrégation, EPC, O&M, AMO), closing bancaire, assurances, dossier EXE validé, pull-out tests
- Slides typiques additionnelles : "Tour de table financier", "Closing achevé", "Contrats clés signés", "Lancement chantier", "Calendrier construction"

---

# J5 — Construction

## 88. Déclaration d'Ouverture de Chantier (DOC)

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Déclaration d'Ouverture de Chantier (DOC)** déposée en mairie par la SPV pour notifier officiellement le démarrage des travaux de construction. Formalité administrative imposée par l'article R. 424-16 du Code de l'urbanisme. Doit être faite **dans les 3 ans suivant la délivrance du PC** (sous peine de péremption).

**Format observé** : PDF formulaire CERFA tamponné, 1-2 pages.

**Indices internes typiques** :
- **En-tête CERFA** : formulaire CERFA n° 13407*XX
- **Titre** : "Déclaration d'ouverture de chantier"
- **Référence PC** : numéro du permis de construire concerné
- **Date d'ouverture du chantier**
- **Identification maître d'ouvrage** : SPV
- **Cachet mairie** : tampon avec date de dépôt

**Nommage probable** : `DOC_[CodeProjet]_[date].pdf`, `Declaration_ouverture_chantier_[CodeProjet].pdf`.

---

## 89. Plans d'exécution validés

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon

### Description

**Plans d'exécution validés** par l'AMO et le bureau de contrôle, à jour pour le chantier. Sous-ensemble du dossier EXE (cf. doc #83) qui évolue pendant le chantier avec des révisions (Ind A → Ind B → Ind C…) suite aux adaptations terrain.

**Format observé** : DWG + PDF, multi-fichiers organisés par lots.

**Indices internes typiques** :
- **Cartouche** : `Phase : EXE`, indice révision, **mention "BPE" (Bon Pour Exécution)**
- **Validation** : VISA AMO + VISA bureau de contrôle dans cartouche
- **Date de validation** récente (postérieure au lancement chantier)

**Nommage** : multiples plans dans dossier `Plans_EXE_[CodeProjet]/` avec révisions.

**Stratégie** : LLM marque "Présent" si plans EXE récents et validés (postérieurs à la DOC).

---

## 90. Rapport bureau de contrôle (VISA)

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport du bureau de contrôle technique** (Apave, Veritas, Socotec, Dekra, Qualiconsult) attestant de la conformité des plans d'exécution et des travaux aux normes techniques applicables (Eurocodes, normes électriques NFC 15-100, NFC 13-100, NFC 13-200, NFC 14-100, etc.).

**Format observé** : PDF officiel bureau de contrôle, 10-30 pages.

**Indices internes typiques** :
- **En-tête bureau de contrôle** : logo Apave / Bureau Veritas / Socotec / Dekra / Qualiconsult
- **Titre** : "Rapport de contrôle" ou "Rapport initial de contrôle technique" + référence VISA
- **Référence** : numéro de mission, date d'établissement
- **Sections** : Périmètre de la mission (LP - Solidité, SEI - Sécurité incendie, etc.), Observations, Conclusions
- **VISA** : tableau récapitulatif des plans visés (numéro, indice, statut Validé/Refusé/Réserves)
- **Signature** : contrôleur technique habilité

**Nommage probable** : `Rapport_VISA_[BureauControle]_[CodeProjet]_[date].pdf`, `Controle_technique_[CodeProjet].pdf`.

---

## 91. Certification carbone des modules

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Certificat d'évaluation carbone des modules** photovoltaïques installés sur la centrale, requis pour les appels d'offres CRE qui imposent un critère carbone (typiquement < 550 kg eqCO2/kWc pour PV au sol). Document émis par le fabricant ou par un organisme certificateur (Certisolis, etc.).

**Format observé** : PDF certificat, 5-15 pages avec annexes.

**Indices internes typiques** :
- **Émetteur** : fabricant des modules (Jinko Solar, JA Solar, LONGi, Trina, Q Cells, etc.) ou organisme certificateur
- **Titre** : "Évaluation carbone simplifiée" ou "ECS" ou "Certification empreinte carbone modules PV"
- **Référence** : numéro de certificat, date de validité
- **Identification module** : référence commerciale, puissance unitaire (Wc), technologie (monocristallin, bifacial, etc.)
- **Valeur carbone** : kg eqCO2 / kWc
- **Conformité** : mention "Conforme au cahier des charges de l'AO CRE [...]"

**Nommage probable** : `Certificat_carbone_[Module]_[Reference].pdf`, `ECS_modules_[CodeProjet].pdf`.

---

## 92. Agréments et décennales installateurs

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Ensemble des **agréments professionnels et attestations décennales** des installateurs intervenant sur le chantier. Comprend typiquement les qualifications QualiPV, Qualifelec, Quali'EnR, OPQIBI, FFB, ainsi que les attestations décennales (cf. doc #82 mais limité aux installateurs PV/électriques).

**Format observé** : multiples PDF.

**Indices internes typiques** :
- **Agréments** : certificats QualiPV (mention "RGE - Reconnu Garant Environnement"), Qualifelec, Quali'EnR
- **Décennales** : cf. doc #82

**Nommage probable** : `Agrement_QualiPV_[Entreprise]_[Annee].pdf`, `Decennale_[Installateur]_[Annee].pdf`.

---

## 93. Déclarations de sous-traitance

- **Jalon** : J5 (Construction)
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

Déclarations de sous-traitance déposées par l'EPC contractor auprès du maître d'ouvrage (SPV) pour valider chaque sous-traitant intervenant sur le chantier. Conforme à la **loi du 31 décembre 1975** relative à la sous-traitance.

**Format observé** : multiples formulaires CERFA ou documents équivalents.

**Indices internes typiques** :
- **Référence** : loi du 31/12/1975, article 3
- **Identification** : entrepreneur principal (EPC) + sous-traitant + maître d'ouvrage (SPV)
- **Périmètre** : nature des travaux sous-traités, montant
- **Validation MOA** : tampon/signature SPV acceptant le sous-traitant

**Nommage probable** : `Declaration_sous_traitance_[Soustraitant]_[CodeProjet].pdf`.

---

## 94. Planning chantier

- **Jalon** : J5 (Construction)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Planning détaillé du chantier** (Gantt) émis par l'EPC contractor ou l'AMO. Précise les phases (préparation, terrassement, fondations, structures, modules, électricité, raccordement, mise en service) avec dates de début/fin et jalons clés.

**Format observé** : PDF (extrait de MS Project ou équivalent), 1-10 pages.

**Indices internes typiques** :
- **Format Gantt** : diagramme à barres horizontales avec dates
- **Phases du chantier** : Préparation, Terrassement & VRD, Fondations, Pose structures, Pose modules, Câblage DC/AC, Postes de transformation et livraison, Raccordement Enedis, Mise en service
- **Jalons** : DOC, Pull-out test conforme, Première table installée, COD (Commercial Operation Date), Réception
- **Émetteur** : EPC contractor ou AMO

**Nommage probable** : `Planning_chantier_[CodeProjet]_v[X].pdf`, `Planning_construction_[CodeProjet].pdf`.

---

## 95. Plan QHSE

- **Jalon** : J5 (Construction)
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Plan QHSE = Qualité, Hygiène, Sécurité, Environnement** du chantier. Document encadrant les mesures de prévention des risques pendant la construction. Imposé par le Code du travail (article R. 4532-44 et suivants pour les chantiers de plus de 10 000 hommes-jours ou impliquant plusieurs entreprises).

**Format observé** : PDF, 20-50 pages.

**Indices internes typiques** :
- **Titre** : "Plan QHSE" ou "Plan Particulier de Sécurité et de Protection de la Santé" (PPSPS) ou "Plan général de coordination" (PGC)
- **Sections** : Identification du projet, Coordonnateur SPS, Analyse des risques par phase, Mesures de prévention, Gestion des déchets, Plan d'évacuation, Premiers secours
- **Référence** : article L. 4532-1 et suivants Code du travail

**Nommage probable** : `Plan_QHSE_[CodeProjet]_[date].pdf`, `PPSPS_[CodeProjet].pdf`.

---

## 96. Architecture SCADA

- **Jalon** : J5 (Construction)
- **Propriété** : Cas par cas
- **Versioning** : Document unique

### Description

**Architecture du SCADA** (Supervisory Control And Data Acquisition) — schéma technique du système de supervision et télégestion de la centrale. Permet de monitorer en temps réel la production, les paramètres techniques (température, irradiance, performance des onduleurs), et de piloter à distance.

**Format observé** : PDF schémas + notes, 10-30 pages.

**Indices internes typiques** :
- **Schémas** : architecture réseau SCADA, position des capteurs (cellules de référence, anémomètres, sondes de température), équipements de communication (PLC, routeurs, modems 4G), liaison avec serveurs centralisés
- **Émetteur** : EPC contractor ou intégrateur SCADA (Solar-Log, Skytron, Meteocontrol, etc.)
- **Référence protocoles** : Modbus TCP, IEC 61850, MQTT, etc.

**Nommage probable** : `Architecture_SCADA_[CodeProjet].pdf`, `Schema_monitoring_[CodeProjet].pdf`.

---

# J6 — Mise en Service (MES)

## 97. CONSUEL

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Attestation CONSUEL** (Comité National pour la Sécurité des Usagers de l'Électricité) — visa de conformité de l'installation électrique délivrée par le CONSUEL. **Préalable obligatoire à la mise en service** par Enedis. Atteste que l'installation respecte les normes électriques (NFC 15-100, NFC 13-100, NFC 13-200, NFC 14-100).

**Format observé** : PDF attestation officielle CONSUEL, 1-3 pages.

**Indices internes typiques** :
- **En-tête** : logo CONSUEL, "République Française"
- **Titre** : "Attestation de conformité" + type (jaune pour résidentiel, bleu pour collectif et tertiaire, vert pour photovoltaïque)
- **Référence** : numéro CONSUEL unique
- **Type d'attestation** : "AC23" (PV avec injection) ou "AC25"
- **Identification installation** : adresse, puissance (kVA), tension de raccordement (BT/HTA)
- **Signature** : organisme agréé ayant visé
- **Mention** : "Cette attestation est valable pour la mise en service par le gestionnaire de réseau"

**Nommage probable** : `Attestation_CONSUEL_[CodeProjet]_[date].pdf`, `CONSUEL_AC23_[CodeProjet].pdf`.

**Piège** : pour les centrales > 36 kVA (donc tous les projets EnerVivo), l'attestation CONSUEL doit être visée par un organisme agréé (non par auto-certification).

---

## 98. Attestation de conformité ENEDIS et DEIE

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Document fusionné** regroupant deux attestations :
1. **Attestation de conformité Enedis** : Enedis valide la conformité du raccordement et du dispositif d'injection
2. **DEIE = Demande d'Établissement de l'Installation Électrique** ou **DEIE = Déclaration d'Exploitation d'Installation Électrique** (selon contexte) — attestation que l'installation est prête à fonctionner

**Format observé** : PDF Enedis officiel, 2-5 pages.

**Indices internes typiques** :
- **En-tête Enedis**
- **Titre** : "Attestation de conformité électrique" ou "Mise en service technique"
- **Référence** : numéro Enedis, PRM (Point de Référence de Mesure)
- **Mention** : "Installation conforme aux exigences de raccordement", "Date de mise en service technique"
- **Caractéristiques techniques validées** : puissance crête, puissance d'injection (kVA), tension, comptage installé

**Nommage probable** : `Attestation_conformite_ENEDIS_[CodeProjet].pdf`, `DEIE_[CodeProjet]_[date].pdf`.

---

## 99. PV de réception chantier

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Procès-verbal de réception du chantier** signé entre la SPV (maître d'ouvrage) et l'EPC contractor. Acte la livraison de la centrale, le démarrage de la garantie de parfait achèvement (1 an), et le cas échéant les **réserves émises** à lever.

**Format observé** : PDF, 5-20 pages avec annexes.

**Indices internes typiques** :
- **Titre** : "Procès-verbal de réception" ou "PV de réception des travaux"
- **Date de réception** : date d'effet juridique de la livraison
- **Parties** : SPV (réceptionnaire) + EPC contractor (entreprise) + AMO (témoin)
- **Réserves** : liste éventuelle des points à reprendre (avec délais)
- **Cas possibles** :
  - **Réception sans réserves**
  - **Réception avec réserves** (cas le plus courant)
  - **Refus de réception** (rare, point bloquant)
- **Référence article 1792-6 du Code civil**
- **Signatures** : SPV + EPC contractor + AMO

**Nommage probable** : `PV_reception_[CodeProjet]_[date]_signe.pdf`, `Reception_chantier_[CodeProjet].pdf`.

**Piège** : version signée uniquement — drafts à ignorer. Vérifier la présence des signatures.

---

## 100. DOE

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**DOE = Dossier d'Ouvrages Exécutés** — ensemble des plans tels qu'exécutés (versions "as-built"), notices techniques, fiches d'équipements, garanties fabricants, schémas électriques définitifs. **Livré par l'EPC contractor à la réception**. Document de référence pour toute l'exploitation et la maintenance future.

**Format observé** : dossier multi-fichiers, plusieurs centaines de pages (souvent organisé en sous-dossiers : Plans, Notices, Garanties, etc.).

**Indices internes typiques** :
- **Titre** : "DOE" ou "Dossier des Ouvrages Exécutés"
- **Sommaire structuré** : Description générale, Plans (implantation, structures, électriques as-built), Notices techniques équipements, Garanties fabricants, Procès-verbaux d'essais, Schémas unifilaires, Plan de mise à la terre
- **Annexes** : DT-DICT du chantier, attestations diverses
- **Cartouche plans** : "TQE" (Tel Que Exécuté) ou "AB" (As-Built)

**Nommage probable** : dossier `DOE_[CodeProjet]/`, fichier sommaire `DOE_sommaire_[CodeProjet].pdf`.

**Stratégie** : LLM marque "Présent" si dossier DOE structuré trouvé avec sommaire et plans as-built.

---

## 101. Rapport tests PR

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport de tests du Performance Ratio (PR)** — mesure de la performance de la centrale (productible réel / productible théorique en conditions standard). Test réalisé après MES sur une période donnée (typiquement 1 mois ou 3 mois) pour valider la performance contractuelle. PR > 80-85% typiquement attendu.

**Format observé** : PDF rapport technique, 20-50 pages.

**Indices internes typiques** :
- **Émetteur** : AMO ou bureau de mesures indépendant
- **Titre** : "Rapport de test Performance Ratio" ou "Test de garantie PR"
- **Méthodologie** : référence IEC 61724-1 (norme internationale mesure performance PV)
- **Période de mesure** : du [date début] au [date fin]
- **Données collectées** : production électrique (kWh), irradiance (kWh/m²), température modules, disponibilité onduleurs
- **Calcul PR** : formule + résultat en %
- **Conclusion** : conformité ou non aux engagements contractuels

**Nommage probable** : `Rapport_PR_[CodeProjet]_[date].pdf`, `Test_Performance_Ratio_[CodeProjet].pdf`.

---

## 102. Rapport tests onduleurs

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Rapport des tests réalisés sur les onduleurs** — vérification du bon fonctionnement de chaque onduleur (rendement, qualité du signal, protections, communication SCADA). Tests fonctionnels et de mise en route effectués par l'installateur ou l'AMO.

**Format observé** : PDF, 10-50 pages avec tableaux de mesures.

**Indices internes typiques** :
- **Marque/modèle onduleurs** : SUNGROW SG350-HX, SMA Sunny Highpower, Huawei SUN2000, etc.
- **Tableau de tests** : pour chaque onduleur (référence, numéro de série), résultats des tests (rendement mesuré, courant DC, tension AC, fréquence, communication OK/KO)
- **Conformité** : statut OK / NOK / À reprendre par onduleur

**Nommage probable** : `Tests_onduleurs_[CodeProjet]_[date].pdf`, `Rapport_essais_onduleurs_[CodeProjet].pdf`.

---

## 103. DAT

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**DAT = Déclaration d'Achèvement des Travaux** déposée en mairie par la SPV à la fin de la construction. Formalité administrative obligatoire (article R. 462-1 du Code de l'urbanisme), parfois appelée DAACT (Déclaration Attestant l'Achèvement et la Conformité des Travaux).

**Format observé** : PDF formulaire CERFA tamponné, 1-3 pages.

**Indices internes typiques** :
- **En-tête CERFA** : formulaire CERFA n° 13408*XX
- **Titre** : "Déclaration attestant l'achèvement et la conformité des travaux (DAACT)" ou "DAT"
- **Référence PC** : numéro du PC concerné
- **Mention** : "Les travaux sont conformes au permis de construire délivré"
- **Identification maître d'ouvrage** : SPV
- **Cachet mairie** : tampon avec date de dépôt
- **Signature** : maître d'ouvrage + architecte si présent

**Nommage probable** : `DAACT_[CodeProjet]_[date].pdf`, `DAT_[CodeProjet]_[date].pdf`.

**Piège** : la mairie a 3 mois pour contester (5 mois pour ERP, sites classés, etc.). Au-delà, la conformité est tacite.

---

## 104. Première facture EDF OA ou PPA

- **Jalon** : J6 (MES)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

Première **facture émise par la SPV** au titre de la vente d'électricité, soit à EDF OA (en tarif réglementé), soit à l'acheteur du PPA (en contrat de gré à gré). Document prouvant la **réalisation effective** des injections et le démarrage du flux financier.

**Format observé** : PDF facture standard.

**Indices internes typiques** :
- **Émetteur** : SPV [Nom projet], SIRET, adresse, RIB
- **Destinataire** : EDF OA ou acheteur PPA
- **Période de facturation** : mois ou trimestre concerné
- **Quantités** : énergie injectée en kWh ou MWh
- **Tarif** : €/MWh appliqué (tarif d'achat ou prix PPA)
- **Montant HT/TTC** : total facturé
- **Date de mise en service** : référence pour les contrats à tarif réglementé
- **Numéro de facture** : F[Année]-[N°]

**Nommage probable** : `Facture_EDF_OA_[Periode]_[CodeProjet].pdf`, `Facture_001_[SPV].pdf`.

**Piège** : la première facture peut intervenir avec un décalage de quelques mois après la MES (le temps que le comptage soit relevé et facturé). Vérifier que c'est bien la **première** facture.

---

# J7 — Clôture (Exploitation et fin de vie)

## 105. Contrat O&M actif avec rapports périodiques

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Versionné par jalon (rapports périodiques)

### Description

**Vérification de l'activité du contrat O&M** (cf. doc #78 signé en J4) avec preuve des prestations réalisées via les **rapports périodiques** émis par le prestataire O&M : reporting mensuel/trimestriel de performance, interventions de maintenance, alertes traitées.

**Format observé** : multiples PDF (rapports périodiques), un par période.

**Indices internes typiques** :
- **Émetteur** : prestataire O&M
- **Titre** : "Rapport O&M mensuel" ou "Rapport trimestriel" + période
- **Sections** : Performance de la centrale (production, PR, disponibilité), Interventions réalisées (préventive/corrective), Alertes traitées, Recommandations
- **Tableaux KPI** : production attendue vs réelle, PR mensuel, taux de disponibilité, MTBF (Mean Time Between Failures)

**Nommage probable** : `Rapport_OM_[Mois]_[Annee]_[CodeProjet].pdf`, `O&M_report_[Periode]_[CodeProjet].pdf`.

**Stratégie** : LLM marque "Présent" si au moins 2-3 rapports périodiques récents trouvés (preuve de continuité de l'O&M).

---

## 106. Plan de démantèlement

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Plan de démantèlement** de la centrale en fin d'exploitation (typiquement après 25-30 ans). Document préparé en amont (souvent dès la phase de développement) précisant les modalités techniques et financières du démontage : étapes, garanties financières (provisionnement), recyclage des matériaux, remise en état du site.

**Référence légale** : arrêté du 5 juillet 2024 (loi APER) qui précise le **montant des garanties financières** à constituer en fonction de la puissance de l'installation.

**Format observé** : PDF, 20-50 pages.

**Indices internes typiques** :
- **Titre** : "Plan de démantèlement" ou "Plan de fin de vie" ou "Décommissioning Plan"
- **Sections** : Description de la centrale (rappel), Méthodologie de démantèlement, Tri et recyclage des matériaux (modules, structures métalliques, onduleurs, câbles), Élimination des déchets dangereux, Garanties financières (montant provisionnés), Remise en état agricole du site
- **Référence Arrêté 5 juillet 2024** : tableau de garantie financière en fonction de la puissance MWc
- **Estimation des coûts** : démantèlement, traitement, remise en état

**Nommage probable** : `Plan_demantelement_[CodeProjet].pdf`, `Decommissioning_plan_[CodeProjet].pdf`.

---

## 107. Certificat recyclage panneaux et acier

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Document unique

### Description

**Certificats de recyclage** émis par les filières spécialisées après démantèlement effectif de la centrale :
- **Modules PV** : filière **PV Cycle France** (éco-organisme agréé pour le recyclage des panneaux PV)
- **Acier / structures** : filière de recyclage métaux (ferrailleurs agréés)
- **Câbles cuivre/aluminium** : filière dédiée
- **Onduleurs et équipements électriques** : filière DEEE (Déchets d'Équipements Électriques et Électroniques)

**Format observé** : multiples certificats PDF (un par filière).

**Indices internes typiques** :
- **Émetteur** : éco-organisme ou centre de recyclage agréé
- **Titre** : "Certificat de recyclage" ou "Attestation de traitement"
- **Quantités traitées** : tonnage, nombre de modules, etc.
- **Date** : date de prise en charge effective des déchets
- **Référence réglementaire** : arrêté du 23 novembre 2020 (REP PV Cycle), code de l'environnement

**Nommage probable** : `Certificat_recyclage_PV_Cycle_[CodeProjet].pdf`, `Attestation_recyclage_acier_[CodeProjet].pdf`.

**Piège** : document attendu seulement **à la fin de l'exploitation effective** (30+ ans après MES). Pour les centrales en exploitation active, ce document est N/A.

---

## 108. PV remise en état agricole

- **Jalon** : J7 (Clôture)
- **Propriété** : Obligatoire
- **Versioning** : Version signée uniquement

### Description

**Procès-verbal de remise en état agricole** du site après démantèlement de la centrale. Atteste que le terrain a été restitué dans un état permettant la reprise immédiate de l'activité agricole (sol décompacté, fondations retirées, clôtures démontées, voiries supprimées si convenu).

**Conforme à l'engagement de réversibilité** imposé par la Loi APER (article L. 314-36 du Code de l'énergie) et la PDB (cf. doc #2).

**Format observé** : PDF, 5-15 pages avec photos et constat.

**Indices internes typiques** :
- **Titre** : "Procès-verbal de remise en état" ou "PV de restitution agricole"
- **Parties** : Emphytéote (SPV) + Bailleur (propriétaire foncier) + parfois huissier ou expert agréé
- **Description état initial avant centrale** vs **état final post-démantèlement**
- **Photos avant/après** : preuves visuelles
- **Constat de réversibilité** : sol décompacté, terre arable restituée, équipements démontés
- **Garantie agronomique** : potentiel agronomique restitué (analyses pédologiques éventuelles)
- **Signatures** : Emphytéote + Bailleur + témoin (huissier/expert)

**Nommage probable** : `PV_remise_en_etat_[CodeProjet]_[date]_signe.pdf`, `Restitution_agricole_[CodeProjet].pdf`.

**Piège** : document **attendu uniquement en fin de vie** de la centrale (après 25-30 ans). N/A pour les projets en exploitation active.

---

# 🤔 Points à clarifier avec Julien

1. **RIB doublon (docs #22 et #30)** : confirmer si même document ou deux RIB distincts attendus
2. **Lettre d'engagement (doc #33)** : à quoi correspond précisément ce document dans la pratique VivEpic ?
3. **DICT (doc #15)** : confirmation jalon J2a (vs Construction habituel) — ✅ confirmé J2a
4. **Avis SDIS** : pas dans le référentiel V11 — à ajouter ? (typiquement attendu en J2a/J2b pour les centrales sol)
5. **PC (Permis de Construire) délivré / Arrêté PC** : pas dans le V11 — fusionné avec Récépissé dépôt PC ? Le document final (arrêté PC) est central pour J3 (calcul des délais de recours)

---

# 📋 Synthèse pour intégration au Excel V12

Lors de l'intégration dans la colonne 7 "Description" du fichier Excel V12 :
- Conserver les sections **Description** + **Format observé** + **Indices internes typiques** + **Nommage** + **Stratégie/Pièges**
- Adapter la longueur selon le doc (les Annexes 3 PDB peuvent être plus courts, les docs versionnés par jalon peuvent référencer les principes communs)
- Possibilité de mutualiser les "principes communs" des docs versionnés par jalon (Plan masse, TADD, Dossier qualif) en une section globale pour éviter répétition
