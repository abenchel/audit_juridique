# EnerVivo Audit

> Outil d'audit juridique des projets photovoltaïques EnerVivo. Scanne le SharePoint d'un projet, identifie chaque document **par son contenu** via LLM, compare avec la liste attendue par jalon (référentiel V11), et produit un rapport interactif.

📖 **Documentation détaillée** : [SESSION.md](./SESSION.md) — architecture, décisions, flow complet.

## Stack

| Couche | Tech |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript strict + Tailwind + NextAuth v5 |
| Auth | Microsoft Entra ID (SSO Outlook) + filtre strict `@enervivo.fr` |
| Backend | FastAPI + Pydantic v2 + SQLAlchemy 2.0 async + Alembic |
| Worker | Celery 5 (broker Redis) — audits longs, audit en masse |
| DB | PostgreSQL 16 (métadonnées + rapport JSONB) |
| Cache | MinIO S3-compatible (PDF 30j auto-purge, quota 5Go) |
| LLM | OpenRouter `anthropic/claude-haiku-4-5` (abstraction → Anthropic direct possible) |
| SharePoint | MSAL app-only + Microsoft Graph API |
| Reverse proxy | Nginx (dev: `localhost:11118`, prod: `audit.enervivo.fr`) |

## Démarrage

```bash
cp .env.example .env
# Remplir : AZURE_AD_CLIENT_SECRET, NEXTAUTH_SECRET (openssl rand -base64 32),
#           OPENROUTER_API_KEY, mots de passe Postgres/Redis/MinIO

make up         # ⭐ Tout en un : 9 services + migrations + seed automatiques
```

Ouvre <http://localhost:11118> → **Se connecter avec Outlook EnerVivo**.

> **Comment ça marche** : un service `init` (one-shot) tourne au premier démarrage, applique `alembic upgrade head` + `python -m scripts.seed`, puis exit. Les services `api`/`worker`/`beat` attendent sa complétion via `service_completed_successfully`. Idempotent : redémarrer la stack ne réinsère rien.

> **Note App Registration** : le redirect URI dev à enregistrer est `http://localhost:11118/api/auth/callback/microsoft-entra-id`. Voir [infra/deployment/azure-app-registration.md](infra/deployment/azure-app-registration.md).

## Commandes utiles

```bash
make logs s=worker        # logs Celery worker
make shell-db             # psql
make backup               # pg_dump → infra/backups/
make test                 # pytest backend
make dev-web              # Next.js hot reload (hors Docker)
```

## Structure

```
apps/
├── web/          Next.js (frontend + NextAuth)
└── api/          FastAPI + Celery (image Docker unique)
    ├── routers/    REST endpoints
    ├── services/   sharepoint/, extraction/, storage/, llm/, audit/, auth/
    ├── tasks/      Celery tasks (audit, mass_audit)
    ├── db/         Models SQLAlchemy + repos + migrations Alembic
    └── config/     settings.py, documents_v11.json (référentiel), projects_seed.json
packages/
└── shared-types/   Types TS générés depuis Pydantic
infra/
├── docker-compose.yml      8 services prod
├── docker-compose.dev.yml  override hot reload
├── nginx/                  reverse proxy (11118 dev, 80/443 prod)
└── deployment/             azure-app-registration.md, minio-lifecycle.md, backup.md
```

## Référentiel V11

Le fichier `apps/api/config/documents_v11.json` est généré depuis `EnerVivo_Documents_Jalon_V11.xlsx` :

```bash
.venv/bin/python apps/api/scripts/convert_excel_to_json.py \
    --in ../EnerVivo_Documents_Jalon_V11.xlsx \
    --out apps/api/config/documents_v11.json
```

107 documents sur 9 jalons (Avant J1, J1, J2a, J2b, J3, J4, Construction, MES, Cloture).

## Audit — comment ça marche

1. **Listing** SharePoint (récursif via Graph API ou mock)
2. **Pour chaque fichier en parallèle (10 max)** :
   - Téléchargement bytes (RAM)
   - SHA-256
   - Check cache Postgres : déjà classifié ? → réutilise (économie LLM 100%)
   - Sinon : MinIO put + extraction texte (3000 head + 1000 tail) + LLM
3. **Matching** trouvés ↔ référentiel V11 par type, scoring 70/40 (configurable)
4. **Rapport JSONB** complet sauvé dans `audits.result`, affiché en React

Pendant l'exécution, **SSE** via Redis pub-sub `audit:{id}` → progression live.

## Tests

```bash
cd apps/api
pytest -v
```

- `test_domain_filter.py` : 9 cas du filtre `@enervivo.fr`
- `test_extraction.py` : extraction PDF/DOCX + truncate
- `test_classifier.py` : LLM mocké (respx)

## Documentation déploiement

- [Azure App Registration](infra/deployment/azure-app-registration.md)
- [MinIO lifecycle / quota](infra/deployment/minio-lifecycle.md)
- [Backup Postgres](infra/deployment/backup.md)

## Roadmap

- v1.0 (cette release) : auth Entra, audit juridique, SharePoint real, rapport interactif
- v1.1 : audit en masse via Celery beat (planifié hebdo)
- v2.0 : OCR Tesseract, audit technique, audit financier, intégration au CRM EnerVivo

## Licence

Confidentiel — usage interne EnerVivo.
