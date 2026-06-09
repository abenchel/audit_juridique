# EnerVivo Audit — Makefile
# Usage: make <target>

# BuildKit enabled pour caching agressif (10x plus rapide)
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

DC = docker compose -f infra/docker-compose.yml --env-file .env
DCDEV = docker compose -f infra/docker-compose.yml -f infra/docker-compose.dev.yml --env-file .env
# Web-dev : SEUL le frontend en hot-reload, backend en image prod stable.
DCWEB = docker compose -f infra/docker-compose.yml -f infra/docker-compose.web-dev.yml --env-file .env

.PHONY: help up up-dev up-web-dev down restart logs ps build pull \
        migrate revision seed test lint typecheck format \
        shell-api shell-web shell-db shell-redis \
        dev-web dev-api worker beat flower \
        clean reset-db backup purge-cache find-hash

help:
	@echo "EnerVivo Audit — commandes disponibles"
	@echo ""
	@echo "  Stack Docker (tout-en-un):"
	@echo "    up              ⭐ Lance toute la stack — migrate + seed automatiques"
	@echo "    up-dev          Avec hot-reload (web + api + worker)"
	@echo "    up-web-dev      Hot-reload FRONTEND seul (backend en image prod stable)"
	@echo "    down            Arrête tous les services"
	@echo "    restart         Restart complet"
	@echo "    logs [s=NAME]   Logs (option: service spécifique)"
	@echo "    ps              Liste les services"
	@echo "    build           Rebuild les images"
	@echo ""
	@echo "  Base de données (manuel — déjà fait au boot):"
	@echo "    migrate         Re-applique les migrations Alembic"
	@echo "    revision m=...  Génère une nouvelle migration"
	@echo "    seed            Re-insère les projets (idempotent)"
	@echo "    reset-db        ⚠️  Drop + recrée le schéma"
	@echo "    backup          pg_dump dans infra/backups/"
	@echo ""
	@echo "  Cache de classification LLM (par file_hash, table classified_documents):"
	@echo "    find-hash name=X   Affiche le(s) hash SHA-256 d'un fichier (par nom, ILIKE)"
	@echo "    purge-cache hash=Y Purge le cache LLM d'un fichier → re-classifié au prochain audit"
	@echo ""
	@echo "  Dev local (sans Docker):"
	@echo "    dev-web         Next.js dev server"
	@echo "    dev-api         FastAPI uvicorn reload"
	@echo "    worker          Celery worker"
	@echo "    beat            Celery beat"
	@echo ""
	@echo "  Qualité:"
	@echo "    test            pytest + tests TS"
	@echo "    lint            ruff + eslint"
	@echo "    typecheck       mypy + tsc"
	@echo "    format          ruff format + prettier"
	@echo ""
	@echo "  Shells:"
	@echo "    shell-api       Shell dans le conteneur api"
	@echo "    shell-web       Shell dans le conteneur web"
	@echo "    shell-db        psql"
	@echo "    shell-redis     redis-cli"

up:
	@if [ ! -f .env ]; then echo "❌ .env manquant — copie .env.example et remplis les secrets"; exit 1; fi
	$(DC) up -d --build
	@echo ""
	@echo "✓ Stack démarrée. Attente du init (migrate + seed)…"
	@$(DC) logs -f init &
	@PID=$$!; \
	while [ "$$($(DC) ps init --status exited --quiet)" = "" ]; do sleep 2; done; \
	kill $$PID 2>/dev/null || true
	@echo ""
	@echo "✓ Stack prête → http://localhost:$${PUBLIC_PORT:-11118}"
	@echo "  • API docs    : http://localhost:$${PUBLIC_PORT:-11118}/api/docs"
	@echo "  • Flower      : http://localhost:$${PUBLIC_PORT:-11118}/flower"
	@echo "  • MinIO admin : http://localhost:9001 (en mode dev)"

up-dev:
	$(DCDEV) up -d --build

# Frontend en hot-reload, backend (api/worker/...) en image prod stable.
# Idéal pour itérer sur le front sans rebuild et sans le piège venv du mode dev.
up-web-dev:
	$(DCWEB) up -d --build
	@echo ""
	@echo "✓ Frontend en hot-reload → http://localhost:$${PUBLIC_PORT:-11118}"
	@echo "  Modifie apps/web/**/*.tsx|css → rechargement à chaud, pas de rebuild."
	@echo "  Backend (api/worker) tourne en image prod stable."

down:
	$(DC) down

restart: down up

logs:
	@if [ -n "$(s)" ]; then $(DC) logs -f $(s); else $(DC) logs -f; fi

ps:
	$(DC) ps

build:
	$(DC) build

pull:
	$(DC) pull

migrate:
	$(DC) exec api alembic upgrade head

revision:
	@if [ -z "$(m)" ]; then echo "❌ Usage: make revision m=\"description\""; exit 1; fi
	$(DC) exec api alembic revision --autogenerate -m "$(m)"

seed:
	$(DC) exec api python -m scripts.seed

reset-db:
	@echo "⚠️  Confirmer en tapant 'yes': " && read ans && [ "$$ans" = "yes" ]
	$(DC) exec postgres psql -U $${POSTGRES_USER} -d $${POSTGRES_DB} -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	$(MAKE) migrate
	$(MAKE) seed

backup:
	mkdir -p infra/backups
	$(DC) exec -T postgres pg_dump -U $${POSTGRES_USER} $${POSTGRES_DB} | gzip > infra/backups/dump-$$(date +%Y%m%d-%H%M%S).sql.gz
	@echo "✓ Backup créé dans infra/backups/"

# Retrouve le hash SHA-256 d'un fichier par son nom (cache LLM = clé file_hash).
# Usage: make find-hash name="ATTESTATION_STANDARD"
# NB techniques : (1) POSTGRES_USER/DB sont résolus DANS le conteneur (sh -c),
# absents de l'env de make côté hôte. (2) Le SQL passe par STDIN (echo | psql),
# car psql -c n'interpole PAS les variables :'var' — seul le mode stdin/-f le
# fait. (3) Le nom est passé via -e (FNAME) et lié par psql -v → pas d'injection.
find-hash:
	@if [ -z "$(name)" ]; then echo "❌ Usage: make find-hash name=\"nom du fichier\""; exit 1; fi
	@$(DC) exec -T -e FNAME='%$(name)%' postgres sh -c \
		'echo "SELECT DISTINCT file_hash, file_name, classified_type, confidence FROM classified_documents WHERE file_name ILIKE :'"'"'fname'"'"' ORDER BY file_name;" \
		 | psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -P pager=off -v fname="$$FNAME"'

# Purge le cache de classification LLM d'UN fichier (par file_hash) → forcer une
# nouvelle réponse du LLM au prochain audit. Le cache OpenRouter (prompt système,
# TTL 5 min) n'affecte PAS la réponse au fichier et s'auto-purge : c'est BIEN ce
# cache Postgres par hash qui « fige » une classification.
# Usage: make purge-cache hash=<sha256 64 chars>   (récupéré via `make find-hash`)
purge-cache:
	@if [ -z "$(hash)" ]; then echo "❌ Usage: make purge-cache hash=<sha256>  (utilise 'make find-hash name=...' pour le trouver)"; exit 1; fi
	@$(DC) exec -T -e HASH='$(hash)' postgres sh -c \
		'echo "DELETE FROM classified_documents WHERE file_hash = :'"'"'h'"'"';" \
		 | psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -v ON_ERROR_STOP=1 -P pager=off -v h="$$HASH"'
	@echo "✓ Cache LLM purgé pour le hash $(hash) — le fichier sera re-classifié au prochain audit."

dev-web:
	cd apps/web && pnpm dev

dev-api:
	cd apps/api && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

worker:
	cd apps/api && uv run celery -A celery_app worker --loglevel=info

beat:
	cd apps/api && uv run celery -A celery_app beat --loglevel=info

flower:
	cd apps/api && uv run celery -A celery_app flower --port=5555

test:
	cd apps/api && uv run pytest -v
	cd apps/web && pnpm test --if-present

lint:
	cd apps/api && uv run ruff check .
	cd apps/web && pnpm lint

typecheck:
	cd apps/api && uv run mypy . || true
	cd apps/web && pnpm typecheck

format:
	cd apps/api && uv run ruff format .
	cd apps/web && pnpm format --if-present

shell-api:
	$(DC) exec api bash

shell-web:
	$(DC) exec web sh

shell-db:
	$(DC) exec postgres psql -U $${POSTGRES_USER} -d $${POSTGRES_DB}

shell-redis:
	$(DC) exec redis redis-cli

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf apps/web/.next apps/web/node_modules
	rm -rf node_modules
	@echo "✓ Cleaned"
