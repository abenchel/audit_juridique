# EnerVivo Audit Juridique — Brief de présentation

> Document autonome conçu pour briefer Claude (ou un humain) sur l'ensemble du projet en une seule lecture. Aucune référence externe nécessaire pour comprendre.

---

## 1. Le problème métier

**EnerVivo** développe des projets photovoltaïques agrivoltaïques en France (~323 projets sous gestion). Chaque projet traverse **9 jalons** réglementaires/contractuels, et chaque jalon exige un ensemble précis de documents administratifs/juridiques/techniques (promesses de bail, CU, PC, attestations MSA, statuts SPV, contrats EPC, etc.).

Aujourd'hui, **vérifier qu'un projet a bien tous les documents requis à un jalon donné** se fait à la main par les chefs de projet, en naviguant SharePoint à la souris. Sur 107 docs attendus par projet × 323 projets, c'est intractable et source d'erreurs (PDB manquant qui bloque un raccordement, MSA non récupérée qui plante la qualification AgriPV…).

**But du produit** : un audit automatisé qui, en 1 clic, scanne le dossier SharePoint d'un projet, identifie chaque fichier (LLM), le rattache à un type attendu du référentiel, et produit un rapport `present / ambiguous / missing / not_applicable` pour les 107 docs des 9 jalons.

---

## 2. Les 9 jalons et le référentiel V12

| Jalon | Sens métier | # docs |
|---|---|---:|
| Avant J1 | Lettre d'intention initiale | 1 |
| J1 | Validation par le comité d'investissement | 4 |
| J2a | Pré-instruction administrative (CU, propriété, identité) | 27 |
| J2b | Dépôt permis de construire / DP | 15 |
| J3 | Validation finale (PV huissier, raccordement, financement) | 21 |
| J4 | Pré-construction (contrats, assurances, EXE) | 18 |
| J5_Construction | Travaux | 9 |
| J6_MES | Mise en service | 8 |
| J7_Cloture | Clôture projet | 4 |
| **Total** | | **107** |

**Source de vérité** : `260518_Document_par_Jalon_V12.xlsx` → converti en `documents_v12.json` par `scripts/convert_excel_to_json.py`. Colonnes : `# | Jalon | Document | PROPRIETE | Type de versioning | Jalons concernes | Description | Format | Lien_DIBOS_H | Lien_DMONFLANQUIN`.

**Propriété (`propriete`)** — 4 catégories qui déterminent comment l'absence d'un doc est notée :

| Propriété | # | Sémantique si absent |
|---|---:|---|
| `Obligatoire` | 57 | `missing` rouge — compte dans `top_critical_missing` |
| `Cas par cas` | 23 | `not_applicable` (gris N/A) — applicable seulement sous certaines conditions du projet |
| `Annexes 3 PDB` | 12 | `missing` — pièces jointes attendues d'une PDB (sauf MSA non-AgriPV → N/A) |
| `Facultatif` | 15 | `missing` mais pas critique |

**Vérité-terrain** : V12 ajoute deux colonnes `Lien_DIBOS_H` et `Lien_DMONFLANQUIN` qui donnent **pour chaque doc attendu** le chemin SharePoint exact du fichier que l'audit doit trouver, sur 2 projets pilotes. Sert hors-pipeline pour évaluer la qualité de l'audit.

---

## 3. Stack & topologie

```
Browser ─► Nginx :11118 ─┬─► Next.js 14 (NextAuth + Entra ID SSO)     [UI]
                         └─► FastAPI (uvicorn)                         [API + SSE]
                                 │
                                 ├─► Postgres 16 (audits, classified_documents…)
                                 ├─► Redis 7 (Celery broker + pub-sub SSE + flags)
                                 ├─► MinIO (cache bytes PDF, lifecycle 30j)
                                 └─► Celery worker (run_audit — fait le travail)
                                         │
                                         ├─► Microsoft Graph API (SharePoint app-only)
                                         └─► OpenRouter → Claude Haiku 4.5
```

**Une seule origine** `localhost:11118` en dev → pas de CORS, cookies NextAuth fonctionnent. Les bytes PDF ne touchent jamais Postgres ; ils vivent en MinIO (30j auto-purge) et en RAM le temps du traitement.

---

## 4. Algorithme principal

### 4.1 Flow d'un audit

```
Utilisateur clique « Lancer audit complet »
   │
   ▼ POST /api/audits {project_code, jalons=[]}
[FastAPI] INSERT audits status=pending → Celery .delay()
   │
   ▼ EventSource /api/audits/{id}/stream (SSE)
[Celery worker] run_audit(audit_id):
   1. UPDATE audits SET status='running'
   2. SharePoint listing → list[FileMetadata]
      ├── Exclusions : SHAREPOINT_EXCLUDED_FOLDERS (Visuels…)
      └── Garde-fou : ALLOWED_ROOT_PATH=/09-Projets

   3. Pré-filtre _classify_ignored_reason(mime, name)
      ├── ignored : video/audio/archive/cad/gis/technique_binary
      └── auditable : pdf/docx/xlsx/xlsm/xlsb/pptx/csv/eml/msg/jpg/png/heic…

   4. publish SSE "listed" {total: N}

   5. semaphore Semaphore(5) ; tasks = [_wrapped(f) for f in auditable]
      pour chaque fichier en parallèle (5 max) :
        ├── download SharePoint (timeout 300s + retry 3×)
        ├── sha256
        ├── SI cache Postgres (file_hash) HIT → réutilise classification
        ├── SINON :
        │     ├── upload MinIO
        │     ├── extract_text (pdfplumber / docx / xlsx / pptx / image…)
        │     ├── classify(file, sample, audit_type) → {type, confidence, reason}
        │     │   - prompt système = liste exhaustive des 107 types + V12 enrichi
        │     │   - cache_control: ephemeral (5 min) → -76% coût LLM
        │     │   - fallback vision si scan sans texte (PyMuPDF render PNG)
        │     ├── INSERT classified_documents (commit par fichier = stream-write)
        │     └── bytes = None (free RAM avant LLM async)
        └── publish SSE "progress" {done, total, file}

   6. handler = juridique
      expected = handler.load_expected(jalons)        # 107 docs si jalons=[]
      report = match_classified_to_expected(results, expected, project_type)

   7. UPDATE audits SET result=report (JSONB), status='completed'
   8. publish SSE "completed"
```

**Robustesse** :
- Cache cross-audit par `file_hash` → un KBis modèle déjà vu = 0 appel LLM.
- Stream-write : crash worker = on garde ce qui a été fait, l'UI montre rapport partiel.
- Annulation propre via flag Redis `audit:{id}:cancel`.
- Progression résiliente au refresh : snapshot Redis (TTL 24h) sur `audit:{id}:done/total/current_file`.

### 4.2 Classification (par fichier)

**Tier de confiance** :
```
confidence ≥ 70 → "present"           (vert)
40 ≤ conf < 70 → "ambiguous"          (orange, revue manuelle)
conf < 40      → "missing"            (rouge, fichier non rattaché)
```

Seuils tunables via env `CONFIDENCE_THRESHOLD_PRESENT/AMBIGUOUS`.

### 4.3 Matching (rapport final)

Pour chaque doc attendu `e` du référentiel :
1. Filtrer classifications dont `classified_type == e.name` (normalisé sans accents, lowercase).
2. Garder celles `tier ∈ {present, ambiguous}`.
3. Statut final :
   - 0 trouvé + `propriete == "Cas par cas"` → `not_applicable` (gris N/A)
   - 0 trouvé + MSA + projet ≠ AgriPV → `not_applicable`
   - 0 trouvé sinon → `missing`
   - 1+ trouvés tous `present` → `present`, `found_files=[…]`
   - Au moins un `ambiguous` → `ambiguous`

Plusieurs fichiers peuvent matcher le même attendu (ex. 3 CR RDV maire) — tous listés. Les fichiers classés qui ne matchent aucun attendu vont en `orphans` → section « Fichiers non identifiés ».

---

## 5. Le prompt LLM (cœur métier)

### 5.1 System prompt — généré dynamiquement depuis `documents_v12.json`

```
Tu es un expert en analyse de documents juridiques et techniques liés aux projets
photovoltaïques agrivoltaïques en France.

Voici la liste EXHAUSTIVE des types de documents possibles dans un dossier projet EnerVivo :

- LOI signee  (dossier : 4-Documents Administratifs/2-LOI ; ext : .pdf)
- PDB signee  (dossier : 4-Documents Administratifs/6-Bail/PDB ; ext : .pdf)
- Plan de masse version J1
- TADD version J1  (ext : .xlsx, .xlsb)
- Dossier de qualification J1  (ext : .pptx)
- Certificat d'urbanisme opérationnel (CU)
- ... (107 entrées au total)
- Autre / Non identifié

⚠️ Hints (dossier/ext/note) PUREMENT INDICATIFS — jamais des filtres stricts.
Les vrais projets s'organisent librement.

Règles strictes :
1. Réponds UNIQUEMENT en JSON valide : {"type", "confidence", "reason"}.
2. "type" copié EXACTEMENT depuis la liste.
3. "confidence" entier 0-100 :
   - ≥ 80 : signature/cachet officiel, contenu sans ambiguïté
   - 60-79 : contenu correspond mais signatures manquantes
   - 40-59 : indices faibles, plusieurs candidats
   - < 40 : doute majeur
4. "reason" : 1 phrase FR, max 25 mots.
5. Aucun markdown, aucun texte hors JSON.

Exemple :
{"type": "PDB signee", "confidence": 92, "reason": "Acte intitulé Promesse de Bail signé par bailleur et preneur avec parcelles cadastrales."}

---

📚 RÉFÉRENTIEL ENRICHI V12 — fiches métier détaillées par type :
[descriptions_part1.md + descriptions_part2.md : ~3000 lignes
 — définition, format, indices internes, conventions de nommage,
 pièges classiques pour CHAQUE type]
```

**Caching ephemeral OpenRouter** (5 min TTL) → 1ᵉʳ fichier facturé ~1200 tokens, suivants ~300 tokens chacun. Coût audit 300 fichiers : 0,375 $ → **0,091 $** (−76 %).

### 5.2 User prompt (texte)

```
Nom du fichier : 2024-02-27 Promesse bail emphytéotique - IBOS - signée-courrier.pdf
Chemin SharePoint : /09-Projets/DIBOS_H/4 - Documents Administratifs/Promesse de Bail/…

Extrait du contenu :
"""
[2000 premiers caractères du PDF]
…
[800 derniers caractères]
"""

Identifie le type de ce document.
```

### 5.3 User prompt (vision — scans sans texte)

```
Nom du fichier : IMG_4523.jpg
Chemin SharePoint : /09-Projets/DIBOS_H/4 - Documents Administratifs/CNI/…

Ce PDF est un SCAN sans couche texte extractible. Les pages t'ont été jointes en images.
Lis le titre, l'en-tête, les cachets et les signatures pour identifier le type.

Identifie le type de ce document.
```

Images normalisées par Pillow en JPEG ≤1568px ≤4 MB (cap multimodal Claude).

---

## 6. Modèle de données

```
users(id UUID PK, email UNIQUE, full_name, role)
   └─ Pas de password — auth Entra ID

projects(code PK, name, type, sharepoint_url, current_jalon, …)
   │
   └─ audits(id UUID PK, project_code FK, audit_type, jalons text[],
             status: pending|running|completed|failed,
             result JSONB,            ◄── rapport complet AuditReport ici
             error_message,
             started_at, completed_at,
             triggered_by FK users)
       │
       └─ classified_documents(id PK, audit_id FK CASCADE,
                               sharepoint_url, sharepoint_path, file_name, file_size,
                               file_hash CHAR(64),     ◄── INDEX, cache cross-audit
                               mime_type,
                               classified_type,        ◄── label retourné par LLM
                               confidence (0-100),
                               reason,
                               status, jalon, llm_model,
                               classified_at)
           INDEX (file_hash, classified_type)
```

**Règle d'or** : zéro byte de PDF en Postgres. MinIO uniquement, 30j auto-purge.

---

## 7. État qualité actuel — DIBOS_H

Audit du 2026-05-24 (avant fix « Cas par cas ») comparé aux **46 fichiers de vérité-terrain V12** :

| Verdict | # | % |
|---|---:|---:|
| ✅ Fichier **exact** trouvé | 18 | 39 % |
| ⚠️ Autre fichier classé (faux positif / multi-candidats) | 8 | 17 % |
| ❌ Manqué (`missing` ou `not_applicable`) | 18 | 39 % |
| ❓ Doc attendu absent du référentiel V11 → V12 (`DT/DICT résumé`) | 2 | 4 % |

### Patterns d'erreur identifiés

1. **Multi-instances d'un même attendu mal géré** : `PV 1er/2ème/3ème passage huissier` — un seul constat trouvé, les 2 autres comptés missing au lieu de réutiliser le même fichier (ou détecter qu'il manque vraiment des passages distincts). Idem `Titre de propriété` vs `Attestation de vente notaire` (même fichier physique attendu pour 2 entrées).
2. **Versioning par jalon (Plan de masse, TADD, Dossier de qualification)** : confusion fréquente entre J1/J2a/J2b/J3/J4 — le jalon **n'est jamais explicite dans le nom du fichier**. Annexe disponible : `_APS_` → J1, `_APD_` → J2a, `_PC_/_DP_` → J2b, `_EXE_/_PRO_` → J3/J4. Pas encore intégré au prompt en règle dure.
3. **`.xlsb` anciens TADD** : tous ratés. Extracteur `pyxlsb` peut-être en cause (peu de texte exploitable pour le LLM ?).
4. **JPG identité (CNI, livret famille, RIB, LOI signée)** : ratés via vision LLM. Pillow re-encode → soit l'image perd en lisibilité, soit le prompt vision n'est pas assez explicite.
5. **2 docs absents** (`DT résumé`, `DICT résumé`) : étaient pas dans V11, sont dans V12 → corrigé par régénération `documents_v12.json` depuis V12.

### Fix « Cas par cas » récent

23 docs `Cas par cas` (Devis EPA, ICPE, Rapport EPA final, Architecte si PC, CDPENAF, CETI, Candidature tarif, G2PRO, Contrats agrégation/EPC > 5 MWc/AMO, Assurance DO, Décennales, Pull out test, Sous-traitance, QHSE, SCADA, etc.) ne génèrent plus de faux « missing » s'ils ne s'appliquent pas au projet. Bascule en `not_applicable` (badge gris « N/A ») avec note métier visible dans l'UI pour que le BE juge.

**Compromis assumé** : un vrai oubli sur un « Cas par cas » devient un N/A discret au lieu d'un missing rouge. L'auditeur humain doit lire les N/A pour vérifier que la condition ne s'applique vraiment pas. Alternative non implémentée : un statut `conditional_missing` distinct (orange clair).

---

## 8. Coûts mesurés

| Métrique | Valeur |
|---|---|
| Coût LLM moyen / fichier (avec cache) | ~0,0003 $ |
| Audit 300 fichiers | ~0,09 $ |
| Mass audit 323 projets, pire cas | ~97 $ |
| Mass audit 323 projets, cache cross-projet effectif | < 5 $ |
| Temps / fichier (gros PDF) | 35–45 s |
| Temps audit 300 fichiers | ~35 min |

---

## 9. Points ouverts / questions à trancher

1. **Versioning par jalon** : faut-il un module post-traitement dédié qui regarde le nom (`_APS_`, `_APD_`, `_PC_`, `_EXE_`) et la date pour ré-affecter un Plan de masse / TADD / Dossier qualif au bon J1/J2a/J2b/J3/J4 ? Aujourd'hui c'est le LLM qui devine via les descriptions enrichies — résultats inégaux sur DIBOS_H.
2. **Statut `conditional_missing`** : un 7ᵉ statut entre `missing` (rouge) et `not_applicable` (gris) pour les « Cas par cas » non trouvés mais visiblement applicables ? Implique changement type + UI + couleur.
3. **Multi-instances** : comment modéliser proprement `PV 1er/2ème/3ème passage huissier` ? Trois entrées distinctes au référentiel, mais le LLM ne sait pas distinguer le 1er du 2ème dans un PDF. Option : fusionner en 1 entrée « PV passages huissier » avec contrainte `min_files=3`.
4. **Extraction `.xlsb`** : pyxlsb extrait-il bien le contenu utile ? À vérifier sur un TADD réel pour comprendre pourquoi 100 % des `.xlsb` sont ratés.
5. **Vision JPG identité** : reformuler le prompt vision pour mentionner explicitement « cherche CNI / RIB / livret de famille / signature » ? Aujourd'hui c'est générique.
6. **Régénération référentiel** : la V13 arrivera. Le pipeline `xlsx → json → prompt LLM` est solide, mais il faut documenter le contrat de colonnes attendu (`PROPRIETE`, `Description`, `Format`).
7. **Auto-refresh frontend** : rapport partiel pendant la run nécessite refresh manuel. Brancher polling client ou event SSE `partial_ready` ?
8. **OCR** : `extraction/ocr.py` est un stub. Si volume de scans grandit, brancher Tesseract en fallback avant la vision LLM (moins cher).

---

## 10. Ce qui marche bien (à garder)

- Cache hash cross-audit + cache MinIO → coût marginal d'un re-audit ≈ 0.
- Prompt caching OpenRouter ephemeral → −76 % coût LLM.
- Pré-filtre `_classify_ignored_reason` → −30 à −50 % bande passante (pas de download des vidéos / CAD / archives).
- Stream-write + cancel propre + rapport partiel → l'UX est tolérante aux crashs.
- Le prompt système enrichi avec `descriptions_part1.md` + `descriptions_part2.md` injectés en queue cacheable → contexte métier dense sans exploser la facture.

---

## 11. Comment poser une bonne question à Claude après ce brief

Le projet est complexe mais l'architecture est solide. Les questions productives portent sur :

- **Qualité de classification** : « comment améliorer le score 18/46 sur DIBOS_H ? » → on regarde les patterns d'erreur §7.
- **Évolutions référentiel** : « comment ajouter X type de doc ? » → on régénère le JSON + le prompt suit.
- **Performance / coût** : « est-ce qu'on peut classer en batch plutôt que 1 par 1 ? » → modèle de coût §8.
- **Cas métiers nouveaux** : « comment gérer un nouveau type de projet (S21, ACC, AMI) ? » → conditionnels §4.3, champ `propriete=Cas par cas` §2.

Les questions moins productives (réponse déjà dans le brief) :
- « Pourquoi pas Postgres pour les PDFs ? » → §3 règle d'or.
- « Pourquoi Claude Haiku ? » → §5.1, ratio coût/qualité validé en prod.
- « Pourquoi SSE ? » → §4.1, l'audit prend 35 min, EventSource gère la reconnexion.
