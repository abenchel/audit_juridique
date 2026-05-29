# EnerVivo Audit Juridique — Architecture & Algorithme

> Document de référence pour un développeur qui prend le projet. Décrit **ce qui se passe** quand un utilisateur clique « Lancer audit complet », du clic jusqu'au rapport JSONB.

---

## 1. Vue à 10 000 m

Un **audit juridique** = comparer le contenu d'un dossier SharePoint projet (`/09-Projets/<CODE>`) à un **référentiel** de 107 documents attendus, ventilés sur 9 jalons (Avant J1 → Clôture), et produire pour chaque attendu un statut `present | ambiguous | missing | not_applicable`.

L'algorithme central est : **classer chaque fichier SharePoint vers 0 ou 1 type attendu via un LLM, puis matcher les classifications aux 107 attendus**.

Trois sous-problèmes :

1. **Lister + télécharger** des fichiers SharePoint (auth app-only Microsoft Graph).
2. **Classifier chaque fichier** (extraction texte → prompt LLM → `{type, confidence, reason}`).
3. **Matcher** les classifications au référentiel V11/V12 (un attendu peut avoir 0..N fichiers, certains attendus sont conditionnels).

---

## 2. Stack & topologie

```
Browser ──► Nginx :11118 ──┬─► Next.js 14 (App Router, NextAuth)   [auth, UI]
                           └─► FastAPI (uvicorn)                    [API REST + SSE]
                                   │
                                   ├─► Postgres 16   (audits, classified_documents, projects, users)
                                   ├─► Redis 7       (Celery broker + pub-sub SSE + cancel flags + progress snapshot)
                                   ├─► MinIO         (cache bytes PDF, lifecycle 30j, sharding {hash[:2]}/{hash})
                                   └─► Celery worker (run_audit task — c'est lui qui fait le vrai travail)
                                           │
                                           ├─► Microsoft Graph API (SharePoint app-only)
                                           └─► OpenRouter (LLM Claude Haiku 4.5 par défaut, abstraction LLMProvider)
```

**Une seule origine** (`localhost:11118`) en dev → pas de CORS, cookies NextAuth fonctionnent.

**Pourquoi Celery et pas un endpoint async direct ?** un audit prend 5–40 min (300 fichiers × ~5 s LLM même avec parallélisme 5). Il faut survivre à un refresh navigateur, d'où la séparation : l'endpoint `POST /api/audits` retourne immédiatement un `audit_id`, le worker tourne en arrière-plan, le client lit la progression via SSE.

---

## 3. Modèle de données

```
users(id, email UNIQUE, full_name, role)
   └─ Pas de password — auth Entra ID uniquement

projects(code PK, name, type, sharepoint_url, current_jalon, …)
   └─ audits(id UUID PK, project_code FK, audit_type, jalons text[],
             status: pending|running|completed|failed,
             started_at, completed_at,
             result JSONB,            ◄── le rapport complet vit ici
             error_message,
             triggered_by FK users)
       └─ classified_documents(id PK, audit_id FK,
             sharepoint_url, sharepoint_path, file_name, file_size,
             file_hash CHAR(64),          ◄── INDEX → cache cross-audit
             mime_type,
             classified_type,             ◄── label retourné par le LLM
             confidence (0-100),
             reason,
             expected_doc_code,           ◄── (actuellement non rempli — voir §11)
             status,
             jalon,
             llm_model,
             classified_at)
         INDEX (file_hash, classified_type) → cache cross-audit
```

**Règle d'or** : aucun byte de PDF en Postgres. MinIO seulement, 30 jours auto-purge. Le rapport final (jusqu'à ~150 ko de JSON) vit dans `audits.result` JSONB.

---

## 4. Référentiel — la source de vérité métier

**Fichier** : `apps/api/config/documents_v12.json` (généré depuis `EnerVivo_Documents_Jalon_V11.xlsx` via `scripts/convert_excel_to_json.py`).

**Forme** :

```jsonc
{
  "jalons": [
    {
      "code": "J1",
      "label": "Jalon 1",
      "documents": [
        {
          "code": "j1-pdb-signee",
          "label": "PDB signee",
          "description": "Promesse de bail signée…",
          "format": ".pdf",
          "obligatoire": true,
          "versioning": "signed_only",
          "conditional": null
        }
      ]
    }
  ]
}
```

**107 documents / 9 jalons** (V11). Le V12 ajoute la colonne `Lien_DIBOS_H` / `Lien_DMONFLANQUIN` qui fournit une **vérité-terrain** par projet — utile pour évaluer la qualité de l'audit, pas pour le faire tourner.

**Référentiel V2 enrichi** : `documents_projet_v2.json` ajoute pour 79/107 docs des hints `(dossier conseillé, ext attendue, note métier)`. Injectés dans le prompt LLM comme **indications**, jamais comme filtres stricts.

**Descriptions enrichies** : `descriptions_part1.md` + (nouveau) `descriptions_part2.md` — fiches métier par type de document (définition, pièges, indices). Concaténées dans le system prompt, en queue, pour profiter du **prompt caching OpenRouter (ephemeral, 5 min)**.

**Annexe Plan de masse** : règles spéciales pour distinguer le jalon d'un plan de masse à partir d'indices dans le nom (`_APS_` → J1, `_APD_` → J2a, `_PC_` → J2b, `_EXE_` → J3/J4). À intégrer dans le prompt LLM ou en post-traitement.

---

## 5. Authentification (double couche)

### 5.1 Frontend — NextAuth + Microsoft Entra ID

- Provider `microsoft-entra-id` configuré avec `AZURE_AD_TENANT_ID` (tenant EnerVivo).
- Callback `signIn` rejette tout email qui ne finit pas par `@enervivo.fr` **et** vérifie `token.tid == tenant_id` (bloque les invités B2B d'autres tenants).
- Session JWT signée HS256 avec `NEXTAUTH_SECRET`.

### 5.2 Backend — FastAPI re-vérifie

- `services/auth/jwt_verify.py` décode le JWT avec **le même** `NEXTAUTH_SECRET`.
- `services/auth/domain_filter.py:is_allowed_email()` ré-applique le filtre `@enervivo.fr` (défense en profondeur — si un attaquant forgeait un JWT externe, le filtre rejette).
- `deps.py:get_current_user()` injecte l'utilisateur dans chaque route.

---

## 6. Algorithme principal — `run_audit(audit_id)`

Code : [apps/api/services/audit/engine.py](apps/api/services/audit/engine.py). Vue de haut :

```
async def run_audit(audit_id):
    1.  UPDATE audits SET status='running'                              # endpoint l'a déjà fait
    2.  project = SELECT project FROM audits JOIN projects
    3.  files: list[FileMetadata] = sharepoint.list_files(project.sharepoint_url)
        ├── exclusions : SHAREPOINT_EXCLUDED_FOLDERS (par défaut "Visuels")
        └── garde-fou : ALLOWED_ROOT_PATH = "/09-Projets"

    4.  pré-filtre : _classify_ignored_reason(mime, name)
        ├── ignored.reason ∈ {video, audio, archive, cad, gis,
        │                     technique_binary, presentation?, spreadsheet?, …}
        └── seuls les fichiers "auditables" passent au pipeline

    5.  publish SSE "listed" {total: N}

    6.  semaphore = asyncio.Semaphore(CONCURRENCY=5)
        tasks = [_wrapped(file) for file in auditable_files]
        results = await asyncio.gather(*tasks, return_exceptions=False)

    7.  toutes les CLASSIFIED_DOCUMENTS sont déjà persistées
        (stream-write : commit par fichier, pas de bulk-insert final).

    8.  handler = get_handler(audit_type)            # juridique | technique | financier
        expected = handler.load_expected(jalons)     # documents attendus pour les jalons demandés
        report = match_classified_to_expected(results, expected, project)

    9.  UPDATE audits SET result=report, status='completed'
   10.  publish SSE "completed"
```

### 6.1 `_wrapped(file)` — pipeline par fichier

```
async def _wrapped(file):
    if _is_cancelled():  raise CancelledError                # bouton "Arrêter"

    bytes = await sharepoint.download(file.url)              # timeout 300s + retry 3x
    if len(bytes) > MAX_FILE_SIZE_BYTES:                     # 80 MB → skip, errors.append
        return ErrorFile(...)

    h = sha256(bytes)

    cached = await find_by_hash(h)                           # CACHE CROSS-AUDIT
    if cached:
        classification = cached                              # zéro appel LLM
    else:
        await minio.put(h, bytes)                            # cache bytes 30j

        try:
            sample = extract_text(bytes, mime, name)         # head 2000 + tail 800 chars
        except ScanNoTextError:
            sample = None
            png_pages = render_pdf_pages_to_png(bytes)       # fallback vision (PyMuPDF)
        except ExtractionError as e:
            return ErrorFile(reason=str(e))

        if sample:
            classification = await classify(file, sample)    # LLM texte
        elif is_image(mime) or png_pages:
            classification = await classify_vision(file, imgs)  # LLM multimodal

    bytes = None                                              # ★ libère la RAM
    await INSERT classified_documents (...) commit            # stream-write

    publish SSE "progress" {done: i, total: N, file: name}
    return classification
```

**Points clés** :

- **Cache hash Postgres** (`idx_classified_hash_type`) : si DDESCUNS et DMUZZOLINI ont le même KBis modèle, le 2ᵉ audit ne paye pas le LLM. Économies massives sur les CNI/RIB/Cerfa standards.
- **Stream-write** : un fichier classé = un commit. Crash worker → on a déjà ce qui a été fait.
- **`bytes = None` post-extraction** : libère la mémoire avant le LLM async (OOM fix).
- **`mem_limit: 4G`, `--concurrency=2`** côté Celery worker pour éviter les SIGKILL du OOM killer Docker.
- **Sémaphore applicatif `CONCURRENCY=5`** : 5 fichiers en vol max → équilibre vitesse / déconnexions OpenRouter.

### 6.2 Rapport partiel pendant la run

Une coroutine `_periodic_partial` s'exécute en parallèle du `gather`. Toutes les **30 s** :
- Lit tous les `classified_documents` déjà commit.
- Refait le matching avec le handler.
- Écrit `audits.result = partial_report` (le status reste `running`).

Le frontend lit `result` (s'il est non-null) en mode `running` et affiche un bandeau orange « Rapport partiel ». Refresh manuel pour la mise à jour suivante (auto-refresh : v1.5).

### 6.3 Annulation propre

- `POST /api/audits/{id}/cancel` pose `audit:{id}:cancel = "1"` dans Redis (TTL 1 h) et marque immédiatement `status='failed'` (l'UI se libère instantanément).
- `_is_cancelled()` est lu au début de chaque `_wrapped` avant tout travail. Si `1`, raise `CancelledError`. Les 5 tâches en vol terminent leur fichier courant (~5–10 s), les suivantes s'arrêtent.
- Un dernier rapport partiel est construit avec ce qui a été fait, puis SSE `failed`.

### 6.4 Progression résiliente au refresh

Snapshot Redis (TTL 24 h) à chaque event :
- `audit:{id}:total`, `audit:{id}:done`, `audit:{id}:current_file`.

`GET /api/audits/{id}` renvoie ces 3 valeurs sous `progress_*`. La page audit les utilise comme état initial → la barre redémarre à la bonne position avant même le 1ᵉʳ event SSE.

---

## 7. Extraction de texte — `services/extraction/`

Dispatch par mime + extension (`registry.py`). Chaque extracteur retourne un sample tronqué (`HEAD=2000 + TAIL=800 = ~600 tokens prompt utilisateur, -33% vs initial`).

| Extension | Extracteur | Lib | Notes |
|---|---|---|---|
| `.pdf` | `pdf.py` | `pdfplumber` (lazy import) | Fallback vision LLM si scan sans texte (PyMuPDF render PNG) |
| `.docx`, `.dotx` | `docx.py` | `python-docx` | |
| `.pptx` | `pptx.py` | `python-pptx` | Pour CR mairie en slides |
| `.xlsx`, `.xlsm`, `.xltx` | `xlsx.py` | `openpyxl` | TADD = Excel obligatoire à plusieurs jalons |
| `.xlsb` | `xlsb.py` | `pyxlsb` | Anciens TADD |
| `.csv` | `csv.py` | stdlib + auto-encoding | |
| `.txt`, `.xml` | `text.py` | stdlib | Auto-detect utf-8/cp1252/latin-1 |
| `.eml`, `.msg` | `email.py` | `email` stdlib + `extract-msg` | CR RDV mairie envoyés par mail |
| `.jpg`, `.png`, `.heic`, `.webp` | (vision LLM direct) | Pillow normalise | Re-encode JPEG ≤1568px ≤4 MB pour respecter le cap Claude |

**`_EXT_OVERRIDE`** dans `registry.py` : `{.csv, .txt, .xml, .xlsb}` sont routés par **extension** avant lecture mime, parce que SharePoint Graph renvoie parfois `application/vnd.ms-excel` pour un `.csv` (planterait openpyxl avec « File is not a zip »).

**Pré-filtre `_classify_ignored_reason`** dans `engine.py` : avant le download, on classe les non-auditables :
- `video` (mp4, mov…), `audio`, `archive` (zip, 7z), `cad` (dwg, skp…), `gis` (qgz, shp…), `technique_binary` (pvc PVsyst, mpp Project).
- Ces fichiers vont en `ignored: list[IgnoredFile]` du rapport, jamais téléchargés → **-30 à -50% de bande passante**.

---

## 8. Classification LLM — `services/llm/`

### 8.1 Abstraction `LLMProvider`

`base.py` définit l'interface : `complete_json(messages, model)` et `complete_json_vision(messages, images, model)`.

Deux implémentations interchangeables via `LLM_PROVIDER` :
- `openrouter.py` (défaut) — `anthropic/claude-haiku-4.5` (avec un **point**, pas un tiret).
- `anthropic_direct.py` — fallback si OpenRouter down.

Toutes deux : retry `tenacity` exponentiel (min=2 s, max=15 s, 5 tentatives) sur 429/5xx **et** sur `RemoteProtocolError / ConnectError / ReadError` (OpenRouter coupe parfois sous charge).

Parsing JSON tolérant : strip des fences ` ```json ` que le modèle ajoute parfois.

### 8.2 Prompt système — `prompts/juridique.py`

**Généré dynamiquement** depuis `documents_v12.json` au démarrage (cached LRU). Contient :

1. **Rôle** : auditeur juridique EnerVivo, classe un fichier en un type parmi la liste.
2. **Liste des 107 types** avec : code, label, jalon, format observé, dossier conseillé, note métier. Marqués explicitement **indicatifs** (un projet réel peut avoir une arborescence FR/EN différente, ne JAMAIS pénaliser un mismatch de dossier).
3. **Règles de confidence** :
   - 90–100 : preuve textuelle directe (titre exact, n° Cerfa, formule clé).
   - 70–89 : forte présomption (contexte + nom + format cohérents).
   - 40–69 : ambigu → flag pour revue humaine.
   - 0–39 : aucun lien plausible.
4. **Schéma JSON de sortie** : `{type, confidence, reason}`.
5. **Bloc enrichi** (queue du prompt, cacheable) : `descriptions_part1.md` + `descriptions_part2.md` — fiches métier détaillées par type.

**Prompt caching OpenRouter** :
```python
{"role": "system", "content": system_prompt,
 "cache_control": {"type": "ephemeral"}}
```
TTL 5 min. 1er fichier = ~1200 tokens facturés. Fichiers 2–N (dans 5 min) = ~300 tokens chacun. **−76% de coût** sur un audit de 300 fichiers (0,375 $ → 0,091 $).

### 8.3 User prompt

Pour un fichier :
```
Chemin SharePoint : /09-Projets/DIBOS_H/4 - Documents Administratifs/Promesse de Bail/2024-02-27 …pdf
Nom               : 2024-02-27 Promesse bail emphytéotique - IBOS - signée-courrier.pdf
Taille            : 1.2 MB
Mime              : application/pdf

--- DÉBUT EXTRAIT ---
<2000 premiers caractères>
…
<800 derniers caractères>
--- FIN EXTRAIT ---
```

### 8.4 Vision

Pour images natives et PDFs sans texte (scans), `complete_json_vision` prend `list[tuple[bytes, mime]]` (max ~5 pages). Pillow normalise en JPEG ≤1568 px ≤4 MB (cap multimodal Claude).

---

## 9. Matching — `services/audit/matcher.py`

Entrées :
- `classifications: list[ClassificationResult]` (1 par fichier auditable).
- `expected: list[ExpectedDocument]` (issus du référentiel pour les jalons demandés).
- `project: Project` (pour les conditionnels — type AgriPV, personne physique/morale…).

Sortie : `AuditReport`.

### 9.1 Tiers de confiance — `scoring.py`

```python
def tier(conf):
    if conf >= CONFIDENCE_THRESHOLD_PRESENT:    # 70
        return "present"
    if conf >= CONFIDENCE_THRESHOLD_AMBIGUOUS:  # 40
        return "ambiguous"
    return "missing"          # le fichier ne sera pas rattaché à un attendu
```

Seuils tunables via env (`CONFIDENCE_THRESHOLD_PRESENT`, `_AMBIGUOUS`).

### 9.2 Boucle de matching (logique actuelle)

Pour chaque attendu `e` :
1. Filtrer les classifications dont `classified_type == e.code` (ou matching tolérant via normalisation slug).
2. Garder celles avec `tier ∈ {present, ambiguous}`.
3. Cas :
   - 0 trouvé + obligatoire + conditionnel non rempli → `not_applicable` (ex : MSA si projet ≠ AgriPV).
   - 0 trouvé + obligatoire → `missing` + ajout aux `top_critical_missing`.
   - 0 trouvé + facultatif → `missing` (pas critique).
   - 1+ trouvé(s) tous `present` → `present`, `found_files: [...]`.
   - Au moins un `ambiguous` → `ambiguous`.

### 9.3 Conditionnels

Définis dans le référentiel (`conditional` JSON). Exemples actuels :
- `Attestation MSA chef d'exploitation` : NA si `project.type != "AgriPV"`.
- `Carte Nationale d'Identité / Livret de famille` : NA si propriétaire = personne morale.
- `Extrait Kbis` : NA si propriétaire = personne physique.

(À enrichir au fur et à mesure que de nouveaux cas apparaissent.)

### 9.4 Versioning par jalon

Certains documents (`Plan de masse`, `TADD`, `Dossier de qualification`) ont **5 entrées** dans le référentiel (J1, J2a, J2b, J3, J4). Le LLM voit ces 5 types comme distincts ; le matching n'a rien de spécial à faire **sauf** que la classification est très difficile sans indice de jalon dans le nom (cf. l'annexe « Plan de masse »).

**Stratégie actuelle** : on s'appuie sur le sous-dossier (`old/`, `0 - OLD/`) et les indices `_APS_/_APD_/_PC_/_EXE_` injectés dans les descriptions enrichies. La V12 (vérité-terrain) montre que **ces docs versionnés sont les plus gros foyers d'erreur** (cf. §11 comparaison DIBOS_H).

---

## 10. Endpoints & SSE

| Méthode | Path | Description |
|---|---|---|
| GET | `/api/health` | Healthcheck |
| GET | `/api/auth/me` | Identité utilisateur |
| GET | `/api/projects` | Liste projets |
| GET | `/api/projects/{code}` | Détail projet |
| POST | `/api/audits` | `{project_code, audit_type, jalons[]}` → enqueue Celery, retourne `audit_id` |
| GET | `/api/audits/{id}` | Détail + `progress_*` + `result` JSONB |
| POST | `/api/audits/{id}/cancel` | Pose flag Redis + `status='failed'` immédiat |
| GET | `/api/audits/{id}/stream` | **SSE** — events `{listed, progress, partial_ready, completed, failed}` via Redis pub-sub channel `audit:{id}` |
| GET | `/api/audits/project/{code}` | Historique audits projet |

Nginx : `proxy_buffering off`, `chunked_transfer_encoding on`, `resolver 127.0.0.11` (DNS Docker interne, cache 10 s) pour SSE et hot-rebuild.

---

## 11. État qualité — comparaison DIBOS_H vs vérité-terrain V12

Voir [COMPARAISON_DIBOS_H_V12.md](COMPARAISON_DIBOS_H_V12.md) pour le détail ligne par ligne.

**Audit du 2026-05-24 19:55 vs les 46 fichiers attendus V12** :

| Verdict | # | % |
|---|---:|---:|
| ✅ Fichier exact trouvé | 18 | 39 % |
| ⚠️ Autre fichier classé (faux positif probable, ou rapport multi-candidats) | 8 | 17 % |
| ❌ Manqué (`missing` / `not_applicable`) | 18 | 39 % |
| ❓ Doc attendu absent du rapport (DT / DICT résumé — type pas dans V11) | 2 | 4 % |

**Patterns de défaillance observés** :

1. **Multi-instances d'un même attendu mal géré** : `PV 1er/2ème/3ème passage huissier` — un seul constat trouvé, les 2 autres comptés missing au lieu de réutiliser le même fichier ou détecter qu'il manque vraiment des passages distincts. Idem `Titre de propriété` vs `Attestation de vente notaire` (même fichier physique attendu pour les deux entrées).
2. **Versioning par jalon (Plan de masse, TADD, Dossier de qualification)** : confusion fréquente entre J1/J2a/J2b/J3/J4. Le `260112_PdM CANVA_NDE.pdf` est attendu à J3 **et** J4 (même fichier servi aux deux jalons) ; l'audit ne l'a pas reconnu pour J3.
3. **Formats binaires anciens** : `.xlsb` TADD pour J1/J2a/J2b → tous manqués. À investiguer côté `xlsb.py` (le fichier est-il bien extrait ? le LLM voit-il assez de contenu ?).
4. **JPG d'identité (CNI, livret de famille, RIB)** : missés. La vision LLM est censée gérer mais quelque chose coince — soit l'image n'a pas survécu au resize Pillow, soit le prompt vision ne mentionne pas assez clairement ces types.
5. **`LOI signee`** (.jpg `Offre_Hangar_signe.jpg`) en « Avant J1 » : manqué — vraisemblablement même problème de classification d'image scannée.
6. **2 docs absents du rapport** (`DT - DT résumé`, `DICT - DICT résumé`) : ces types existent dans V12 mais pas dans `documents_v12.json` — il faut **régénérer le référentiel depuis le V12**.

**Action immédiate recommandée** :
```bash
.venv/bin/python enervivo-audit/apps/api/scripts/convert_excel_to_json.py \
    --in 260518_Document_par_Jalon_V12.xlsx \
    --out enervivo-audit/apps/api/config/documents_v12.json
```
(le fichier garde son nom `documents_v12.json` pour compat, mais contient V12).

---

## 12. Coût & performance mesurés

| Métrique | Valeur |
|---|---|
| Coût LLM moyen / fichier | ~0,0003 $ (avec cache OpenRouter) |
| Coût audit 300 fichiers | ~0,09 $ |
| Mass audit 323 projets, pire cas | ~97 $ |
| Mass audit 323 projets, avec cache cross-projet | < 5 $ |
| Temps / fichier (gros PDF) | 35–45 s |
| Temps audit 300 fichiers | ~35 min |

---

## 13. Pièges à connaître

- **Modèle OpenRouter** : `anthropic/claude-haiku-4.5` (**point**, pas tiret). Le tiret → 404.
- **App Reg redirect URI** : `http://localhost:11118/api/auth/callback/microsoft-entra-id` à enregistrer dans Azure.
- **Permissions Graph** : `User.Read` (delegated) + `Sites.Read.All` + `Files.Read.All` (application).
- **`SHAREPOINT_ALLOWED_ROOT_PATH=/09-Projets`** : garde-fou — refuse tout listing hors de cette racine.
- **`output: "standalone"` Next.js abandonné** : le tracer ne copie pas correctement les workspace deps pnpm. Runtime classique `next start` + `node_modules` complet.
- **Server Actions derrière nginx** : nginx doit envoyer `Host = $http_host` (avec port) et `next.config.mjs` autorise `localhost:11118` dans `serverActions.allowedOrigins`.
- **Audit reste en `pending`** : worker mort ? `make logs s=worker`. Audit reste en `running` après crash : `UPDATE audits SET status='failed' WHERE status='running' AND started_at < NOW() - INTERVAL '10 minutes';`.

---

## 14. Pour aller plus loin

- **Reclassify endpoint** : `POST /api/admin/reclassify/{hash}` pour purger une entrée du cache LLM mal classée.
- **OCR** (`extraction/ocr.py` est un stub) : brancher Tesseract si les scans sans texte deviennent fréquents.
- **Heartbeat Celery** : détecter les audits zombies (`running` mais worker mort).
- **Auto-refresh frontend** pendant le rapport partiel : poll client ou event SSE `partial_ready`.
- **Améliorer le matching versionné** : détection robuste J1/J2a/J2b/J3/J4 sur Plan de masse / TADD / Dossier qualif via règles nommées en post-traitement (annexe Plan de masse).
- **Régénérer le référentiel V12** (cf. §11 — 2 docs manquants détectés).
