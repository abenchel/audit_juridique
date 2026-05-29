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

# Keep runtime image minimal
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) venv pré-compilé (deps + bytecode)
COPY --from=builder /app/.venv /app/.venv

# 2) Code source — explicite pour ne PAS embarquer tests/, pyproject.toml,
#    uv.lock, README, etc. dans l'image runtime.
COPY --from=builder /app/main.py /app/celery_app.py /app/alembic.ini ./
COPY --from=builder /app/alembic /app/alembic
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
