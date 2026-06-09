# EnerVivo Audit API — image unique pour api, worker, beat
# Multi-stage : builder uv → runtime slim
# BuildKit cache: lock-first strategy (cache pyproject.toml + uv.lock séparément)

FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never UV_HTTP_TIMEOUT=300
WORKDIR /app

# Copy only the manifest that is guaranteed to exist
COPY pyproject.toml ./

# Install deps with lockfile if present, otherwise resolve from pyproject
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ -f uv.lock ]; then uv sync --frozen --no-install-project --no-dev; else uv sync --no-install-project --no-dev; fi

# Copy app source after dependencies are cached
COPY . .

# Final sync; use frozen only when a lockfile exists
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ -f uv.lock ]; then uv sync --frozen --no-dev; else uv sync --no-dev; fi


FROM python:3.11-slim AS runtime

# Tesseract OCR (binaire système requis par pytesseract) + pack langue français.
# Utilisé UNIQUEMENT pour les PDF scannés (services/extraction/ocr.py) afin de
# joindre le texte OCR au prompt vision. Sans ces paquets, l'OCR est fail-open
# (ocr.py renvoie "" → classification vision seule, comportement antérieur).
# tesseract-ocr-eng est inclus par défaut ; on ajoute -fra pour le corpus FR.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-fra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) venv pré-compilé (deps + bytecode)
COPY --from=builder /app/.venv /app/.venv

# 2) Code source — explicite pour ne PAS embarquer tests/, pyproject.toml,
#    uv.lock, README, etc. dans l'image runtime.
COPY --from=builder /app/main.py /app/celery_app.py /app/alembic.ini ./
COPY --from=builder /app/alembic /app/alembic
# config/ embarque la knowledge base métier V13 injectée dans les prompts LLM :
#   - descriptions_part1.md + descriptions_part2.md (référentiel enrichi V13)
#   - annexe_plan_masse.md (règles passe 2 plan de masse)
#   - Annexe_fichier_TADD.md (règles passe 2 TADD)
#   - documents_v12.json (contenu V13) + documents_projet_v2.json (référentiels)
#   - projects_seed.json (seed) + settings.py
# Les .md ne sont copiés QUE parce que .dockerignore re-inclut !config/*.md.
COPY --from=builder /app/config /app/config
COPY --from=builder /app/db /app/db
COPY --from=builder /app/models /app/models
COPY --from=builder /app/routers /app/routers
COPY --from=builder /app/scripts /app/scripts
COPY --from=builder /app/services /app/services
COPY --from=builder /app/tasks /app/tasks

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Entrypoint surchargé par docker-compose
