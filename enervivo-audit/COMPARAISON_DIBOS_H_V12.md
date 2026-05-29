# Comparaison audit DIBOS_H (2026-05-24 19:55) vs vérité-terrain V12

**Audit ID** : 248b0c42-3bb2-46f6-9d3b-e8905daf3781
**Source vérité-terrain** : `260518_Document_par_Jalon_V12.xlsx` colonne `Lien_DIBOS_H` (46 fichiers attendus)

## Score global

| Verdict | # | % |
|---|---:|---:|
| ✅ Fichier exact trouvé | 18 | 39% |
| ⚠️ Autre fichier classé (faux positif probable, ou multi-candidats) | 8 | 17% |
| ❌ Manqué (rapport dit `missing` / `not_applicable`) | 17 | 37% |
| ❓ Doc attendu absent du rapport (bug référentiel) | 3 | 7% |
| **Total attendus V12** | **46** | 100% |

## Détail par ligne

| # | Jalon | Document attendu | Fichier V12 (vérité) | Fichier trouvé par l'audit | Verdict |
|---|---|---|---|---|---|
| 1 | Avant J1 | LOI signee | `Offre_Hangar_signe.jpg` | `—` | ❌ missing |
| 2 | J1 | PDB signee | `2024-02-27 Promesse bail emphytéotique - IBOS - signée-courrier.pdf` | `2024-02-27 Promesse bail emphytéotique - IBOS - signée-courrier.pdf` | ✅ EXACT |
| 3 | J1 | Plan de masse version J1 | `2024 02 02 DIBOS_Plan_de_masse.pdf` | `2024 02 02 DIBOS_Plan_de_masse.pdf` | ✅ EXACT |
| 4 | J1 | TADD version J1 | `2024 09 23 DIBOSH_TADD_v6_HBA.xlsb` | `—` | ❌ missing |
| 5 | J1 | Dossier de qualification J1 | `2024 02 21 Avant-Projet Agricole IBOS HANGAR_APE.pptx` | `2024 02 21 Avant-Projet Agricole IBOS HANGAR_APE.pptx` | ✅ EXACT |
| 6 | J2a | Certificat d'urbanisme opérationnel (CU) | `DIBOS_Certificat_Urbanisme_cerfa_13410-12.pdf` | `DIBOS_Certificat_Urbanisme_cerfa_13410-12.pdf` | ✅ EXACT |
| 14 | J2a | DT - DT résumé | `2026040800259T_DDC_resume.pdf` | `—` | ❓ doc absent du rapport |
| 15 | J2a | DICT - DICT résumé | `2026040800259T_DDC_resume.pdf` | `—` | ❓ doc absent du rapport |
| 16 | J2a | Plan de masse version J2a | `2024 11 14 ENsend-APD 20240927.pdf` | `Plan_2.jpg` | ⚠️ AUTRE (present) |
| 17 | J2a | TADD version J2a | `2024 11 22_DIBOSH_TADD_v6.1_OFFICIEL_HBA.xlsb` | `—` | ❌ missing |
| 18 | J2a | Carte Nationale d'Identité (CNI) (proprio personne physique) | `2022_08_25_DIBOSH_CNI.jpg` | `—` | ❌ missing |
| 19 | J2a | Copie livret de famille (proprio personne physique) | `2026_05_12_DIBOSH_livret de famille.jpg` | `—` | ❌ missing |
| 21 | J2a | Extrait Kbis a jour (proprio personne morale) | `2024_09_01_DIBOSH_KBIS.pdf` | `2024_09_01_DIBOSH_KBIS.pdf` | ✅ EXACT |
| 22 | J2a | Titre de propriete des parcelles | `2026_01_18_DIBOSH_attestation_propriété.pdf` | `2026_01_18_DIBOSH_attestation_propriété.pdf` | ✅ EXACT |
| 23 | J2a | Attestation de vente notaire (< 2 ans) ou releve de propriete mairie | `2026_01_18_DIBOSH_attestation_propriété.pdf` | `—` | ❌ missing |
| 25 | J2a | Releve d'hypotheques (etat hypothecaire) | `2026_04_01_DIBOSH_état hypothécaire.pdf` | `2026_04_01_DIBOSH_état hypothécaire.pdf` | ✅ EXACT |
| 26 | J2a | Releve parcellaire a jour | `G26023, 409-287W, M1-287, 409-288S & M1-288.pdf` | `2026_05_12_DIBOSH_relevé d'exploitation.pdf, situation_procadastre (48).pdf, Image (25).jpg, Image (26).jpg` | ⚠️ AUTRE (present) |
| 27 | J2a | Lettre de motivation projet agrivoltaique | `2026_05_12_DIBOSH_motivation agricole.docx` | `2026_05_12_DIBOSH_motivation agricole.docx` | ✅ EXACT |
| 29 | J2a | Relevé d'identité bancaire (RIB) pour versement redevances et loyers du bail | `2026_05_12_DIBOSH_RIB.pdf` | `—` | ❓ doc absent du rapport |
| 30 | J2a | Attestation MSA chef d'exploitation (< 6 mois) | `2026_05_12_DIBOSH_relevé d'exploitation.pdf` | `—` | ❌ not_applicable |
| 31 | J2a | Dossier de qualification J2a | `2024 09 23 DIBOSH_Modèle_qualification_projetS21_HBA.pptx` | `—` | ❌ missing |
| 33 | J2b | Compte-rendu RDV SDIS | `Avis SDIS.pdf` | `Avis SDIS.pdf` | ✅ EXACT |
| 38 | J2b | Etude architecte | `2024 05 29 ENsend-CA-CCP01 signé.pdf` | `2024 05 29 ENsend-CA-CCP01 signé.pdf` | ✅ EXACT |
| 39 | J2b | Rapport geometre | `G26023, 409-287W, M1-287, 409-288S & M1-288.pdf` | `G26023, 409-287W, M1-287, 409-288S & M1-288.pdf` | ✅ EXACT |
| 41 | J2b | PRAC recue | `2025-03-24_RAC-PYL-25-000037 - DIBOS-H_Reponse_NDE.pdf` | `—` | ❌ missing |
| 43 | J2b | Recepisse depot PC ou DP | `Arrêté accord PC Enervivo.pdf` | `Arrêté accord PC Enervivo.pdf` | ✅ EXACT |
| 45 | J2b | Plan de masse version J2b | `2024 11 14 ENsend-APD 20240927.pdf` | `—` | ❌ missing |
| 46 | J2b | TADD version J2b | `2024 11 22_DIBOSH_TADD_v6.1_OFFICIEL_HBA.xlsb` | `—` | ❌ missing |
| 47 | J2b | Dossier de qualification J2b | `2024 11 22 DIBOSH_Etude APS_ENERVIVO_HBA.pptx` | `—` | ❌ missing |
| 48 | J3 | ANRNR | `attestation non retrait ibos.pdf` | `attestation non retrait ibos.pdf` | ✅ EXACT |
| 50 | J3 | PV 1er passage huissier | `constat-66090-86441752074062.pdf` | `constat-66090-86441752074062.pdf` | ✅ EXACT |
| 51 | J3 | PV 2eme passage huissier | `constat-66090-86441752074062.pdf` | `—` | ❌ missing |
| 52 | J3 | PV 3eme passage huissier | `constat-66090-86441752074062.pdf` | `—` | ❌ missing |
| 53 | J3 | Présentation de la création SPV à la mairie | `2023-09-20 - Offre Hangar agricole - Enervivo - IBOS.pptx` | `2023 11 03 JSW Slides Mairie.pptx` | ⚠️ AUTRE (ambiguous) |
| 55 | J3 | Statuts SPV signes | `2024-04-22_Courrier de Subsitution_ENERVIVO ENVIROCO2.pdf` | `—` | ❌ missing |
| 58 | J3 | Recepisse de la demande de raccordement / CRD | `2025-03-24_RAC-PYL-25-000037 - DIBOS-H_Reponse_NDE.pdf` | `2025-03-24_RAC-PYL-25-000037 - DIBOS-H_Reponse_NDE.pdf` | ✅ EXACT |
| 59 | J3 | PTF / CRD recue d'ENEDIS | `Fichier échange CRD BT S3R - RAC-PYL-25-000037 - 65409.pdf` | `CRD BT-RAC-PYL-25-000037-DIBOS-H - SARRIAC-BIGORRE.pdf, 2350GPExtRelanceClient1resuraccordsurdevis_2025-07-19_01-10-51.pdf, Renforcement et plan ST avec 14 lots à SARRIAC BIGORRE.pdf` | ⚠️ AUTRE (present) |
| 60 | J3 | PTF / CRD signee | `CRD BT-v2-RAC-PYL-25-000037-DIBOS-H - SARRIAC-BIGORRE.pdf` | `CRD BT-v2-RAC-PYL-25-000037-DIBOS-H - SARRIAC-BIGORRE.pdf` | ✅ EXACT |
| 62 | J3 | Consultations / Devis aupres des fournisseurs | `Devis-IBOS-IEP120224171408 (signed).pdf` | `EnerVivo - 16no. 2050mm - France.pdf, IMG_20250722_102040.jpg, R2 FR 06 - Fiche de renseignements SI Évolution_DIBOS.xlsx, MECOSUN - Fiche Information pour devis - TOUT système - DIBOS.xlsx, IMG_20250722_102104.jpg, IMG_20250722_102202.jpg, 260407_mail offre_RADIX.pdf` | ⚠️ AUTRE (present) |
| 66 | J3 | Plan de masse version J3 | `260112_PdM CANVA_NDE.pdf` | `PERDRIEL ANTOINE -2.pdf, PERDRIEL ANTOINE 17022026 -2.pdf` | ⚠️ AUTRE (ambiguous) |
| 67 | J3 | TADD version J3 | `260303_DIBOS_H_TADD v6.6.9_Version BAC ACIER_Techno Pieux_NDE - Copie.xlsm` | `—` | ❌ missing |
| 68 | J3 | Dossier de qualification J3 | `251013_DIBOS_H_J3_Dossier Qualification_NDE-PAP.pptx` | `251013_DIBOS_H_J3_Dossier Qualification_NDE-PAP.pptx` | ✅ EXACT |
| 82 | J4 | Dossier EXE | `260513_DIBOS PDM EXE Ind A_SDU.pdf` | `260512_DIBOS_Ndc_EXE_Ind A_SDU.pdf, 260423_DIBOS_CC_EXE_Ind A_SDU.pdf, 260423_DIBOS_Ndc_EXE_Ind A_SDU.pdf, 260423_DIBOS_SU_EXE_Ind A_SDU.pdf, 260512_DIBOS_CC_EXE_Ind A_SDU.pdf, 260512_DIBOS_Récap_EXE_Ind A_SDU.pdf, 260512_DIBOS_SU_EXE_Ind A_SDU.pdf` | ⚠️ AUTRE (present) |
| 84 | J4 | Plan de masse version J4 | `260112_PdM CANVA_NDE.pdf` | `260423_DIBOS PDM EXE Ind A_SDU.pdf, 260513_DIBOS PDM EXE Ind A_SDU.pdf, PERDRIEL ANTOINE 17022026 -3.pdf, PERDRIEL ANTOINE 17022026 -4.pdf, RAMPANT PERDRIEL.pdf` | ⚠️ AUTRE (present) |
| 85 | J4 | TADD version J4 | `251128_DIBOS_H_TADD v6.6.3_NDE.xlsm` | `—` | ❌ missing |
| 86 | J4 | Dossier de qualification J4 | `251128_DIBOS_H_J4_Dossier Qualification_NDE-PAP.pptx` | `251128_DIBOS_H_J4_Dossier Qualification_NDE-PAP.pptx` | ✅ EXACT |
