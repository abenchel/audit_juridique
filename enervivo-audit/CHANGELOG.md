# CHANGELOG

> Convention : sections par étape du POC. Chaque étape correspond à un commit dans un futur historique git (l'init git est laissé au soin de l'utilisateur).

## 0.1.1 — `make up` autosuffisant (2026-05-13)

- **Nouveau service `init`** (one-shot) dans `docker-compose.yml` : applique `alembic upgrade head` + `python -m scripts.seed` au premier démarrage, puis exit.
- `api`/`worker`/`beat` ont `depends_on: init: { condition: service_completed_successfully }` → ils ne démarrent qu'après.
- La cible `make up` :
  - Vérifie que `.env` existe (erreur explicite sinon)
  - Build + up tous les services
  - Suit les logs du init en live jusqu'à sa complétion
  - Affiche les URLs prêtes (`/api/docs`, `/flower`, MinIO admin)
- Cibles `make migrate` / `make seed` restent disponibles pour relances manuelles.

## 0.1.0 — Build initial (2026-05-13)

### Étape 1 — Squelette monorepo

- `pnpm-workspace.yaml`, racine `package.json`
- `apps/web/` Next.js 14 + TS strict + Tailwind + shadcn-ready
- `apps/api/` FastAPI + uv (`pyproject.toml`)
- `packages/shared-types/`
- `Makefile` complet (up/down/migrate/seed/test/lint/shell-*)
- `.env.example` exhaustif
- `.gitignore`

### Étape 2 — Docker Compose

- 8 services : nginx, web, api, worker, beat, flower, postgres, redis, minio
- `nginx` exposé sur `localhost:11118` (dev) ; routing `/api/auth/*` → web, `/api/*` → api, `/flower` → flower (basic auth), `/` → web
- Healthchecks Postgres, Redis, MinIO
- Limites MinIO 512M / 0.5 CPU, lifecycle policy auto
- Override `docker-compose.dev.yml` (hot reload)
- Image Docker unique pour api/worker/beat/flower (entrypoints différents)

### Étape 3 — Référentiel V11

- Script `scripts/convert_excel_to_json.py` : Excel → JSON structuré
- Sortie : `config/documents_v11.json` — 107 documents / 9 jalons
- Slugification avec gestion des doublons (#17, #19 alternatives)

### Étape 4 — Schéma DB + Alembic

- Tables : `users`, `projects`, `audits`, `classified_documents`
- Index : `file_hash`, `idx_classified_hash_type`, `project_code`, `status`
- Contraintes : `CHECK confidence BETWEEN 0 AND 100`
- Migration initiale `001_initial_schema.py`
- Repositories : projects, audits, classifications, users
- `db/session.py` AsyncSession factory

### Étape 5 — Seed projets

- `config/projects_seed.json` : DMUZZOLINI + DDESCUNS (AgriPV)
- `scripts/seed.py` idempotent (upsert par code)

### Étape 6 — Auth Entra ID + filtre domaine

- **Frontend** : `lib/auth.ts` NextAuth v5 + `MicrosoftEntraID` provider, `domain_hint=enervivo.fr`, double filtre (email + tenant_id)
- **Frontend** : page `/login` avec bouton unique, `middleware.ts` protection routes
- **Backend** : `services/auth/domain_filter.py`, `jwt_verify.py` (HS256 partagé), `deps.py` (`get_current_user`, `require_admin`)
- Endpoint `GET /api/auth/me`
- Tests `test_domain_filter.py` (9 cas)
- Mode dev `X-User-Email` pour Postman si `ENVIRONMENT=development`

### Étape 7 — SharePoint

- Interface `SharePointClient` async (`base.py`)
- `mock.py` : ~30 fichiers/projet (LOI, PDB signée + draft, CU, 3 CR RDV, plans masse J1/J2a, TADD, Kbis, RIB, CNI, MSA, ICPE, photo, doublons, ambigus)
- `real.py` : MSAL app-only + Microsoft Graph v1.0 (résolution URL→site/drive/folder, walk récursif paginé `@odata.nextLink`)
- Factory `get_sharepoint_client()` selon `SHAREPOINT_MODE`

### Étape 8 — Extraction texte

- `services/extraction/base.py` : `TextExtractor` ABC, `truncate_sample` (3000 + 1000)
- `pdf.py` (pdfplumber, fallback utf-8 pour mock)
- `docx.py` (python-docx avec extraction tables)
- `ocr.py` stub v2 (pytesseract)
- `registry.py` dispatch par mime
- Tests `test_extraction.py`

### Étape 9 — MinIO cache + lifecycle

- `services/storage/minio_client.py` : client cached LRU
- `services/storage/lifecycle.py` : setup auto bucket + lifecycle 30j idempotent (au lifespan de FastAPI)
- `services/storage/cache.py` : `PDFCache.get(hash)/put(hash)` avec sharding `{hash[:2]}/{hash}`, async-wrapped

### Étape 10 — LLM OpenRouter (abstraction)

- `services/llm/base.py` : `LLMProvider` ABC
- `openrouter.py` : httpx async, retry exponentiel 3× via tenacity, parsing JSON tolérant fences ``json``
- `anthropic_direct.py` : provider alternatif (httpx vers api.anthropic.com)
- Factory `get_llm_provider()` selon `LLM_PROVIDER`
- `prompts/juridique.py` : prompt système GÉNÉRÉ depuis `documents_v11.json`
- `classifier.py` : `classify(file, sample, audit_type)` → `(ClassificationResult, model_name)`
- Tests `test_classifier.py` (respx mock)

### Étape 11 — Moteur d'audit + Celery

- `services/audit/scoring.py` : tier 70/40 configurable
- `services/audit/matcher.py` : matching normalisé + conditionnel MSA AgriPV
- `services/audit/types/` : `JuridiqueAudit` (charge V11 LRU), stubs `technique`/`financier`
- `services/audit/engine.py` : `run_audit(id)` orchestrateur complet (listing → 10 parallèles → cache cross-audit → MinIO → extraction → LLM → matching → JSONB)
- Pub-sub Redis `audit:{id}` pour SSE
- `tasks/audit_tasks.py` : `run_audit_task` (retry 2×) + `mass_audit_task`
- `tasks/sync_tasks.py` : stub v2 (sync SharePoint planifié)

### Étape 12 — API REST + SSE

- `routers/projects.py` : `GET /api/projects`, `GET /api/projects/{code}`
- `routers/audits.py` :
  - `POST /api/audits` (push Celery)
  - `GET /api/audits/{id}` (avec `result` JSONB)
  - `GET /api/audits/{id}/stream` (**SSE**, auth via query `?token=`)
  - `GET /api/audits/project/{code}` (historique)
- OpenAPI auto sur `/api/docs`

### Étape 13 — Types TS partagés

- `scripts/generate_ts_types.py` : convertit JSON Schema Pydantic → TS interfaces
- `packages/shared-types/src/manual.ts` : types alignés sur Pydantic (fallback compilable même si script pas tourné)

### Étape 14 — Frontend pages

- `lib/api-client.ts` : client typed côté serveur, signe JWT HS256 inline (jose) pour appeler FastAPI
- `components/Sidebar.tsx` : logo EnerVivo, nav, user avatar, signOut
- `app/(app)/layout.tsx` : protected layout
- `app/(app)/projects/page.tsx` : grille cards (charte EnerVivo)
- `app/(app)/projects/[code]/page.tsx` : détail + Server Action `launchAudit` + historique
- `app/(app)/projects/[code]/audits/[auditId]/page.tsx` : routing par status
- `components/AuditProgress.tsx` (client) : EventSource SSE, barre progression live
- `components/AuditReport/` : **rapport interactif fidèle à v6.html**
  - `Header.tsx` (breadcrumb, titre clamp 40-64px, dl meta)
  - `KpiCards.tsx` (feature cell gradient ink + 3 cells confiance)
  - `Alerts.tsx` (top 3 documents critiques manquants)
  - `JalonProgress.tsx` (progress bars + statuts)
  - `DocumentsTable.tsx` (par jalon, liens cliquables vers SharePoint, raisons LLM)
  - `UnclassifiedSection.tsx` (non identifiés + erreurs techniques)
  - `index.tsx` (composition)

### Étape 15 — Nginx

- Bouclé en étape 2.

### Étape 16 — Doc déploiement

- `infra/deployment/azure-app-registration.md` : créer App Reg, permissions, secret, test
- `infra/deployment/minio-lifecycle.md` : quota, sharding, cache cross-audit, surveillance
- `infra/deployment/backup.md` : pg_dump cron + restauration + off-site rclone
- IONOS-setup intentionnellement **non écrit** (VPS déjà prêt côté utilisateur)

### Étape 17 — README final + CHANGELOG

- `README.md` : quickstart, stack, structure, commandes, roadmap
- `CHANGELOG.md` : ce fichier
- `SESSION.md` : 12 sections (flow complet, archi, schéma, débogage)
