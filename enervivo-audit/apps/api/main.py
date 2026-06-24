"""FastAPI entrypoint — EnerVivo Audit API."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    from services.storage.lifecycle import setup_lifecycle

    await setup_lifecycle()
    app.state.settings = settings
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="EnerVivo Audit API",
        version="0.1.0",
        description="Audit juridique des projets photovoltaïques EnerVivo",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from routers import admin, audits, auth, health, projects

    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(projects.router, prefix="/api")
    app.include_router(audits.router, prefix="/api")
    app.include_router(admin.router, prefix="/api")
    return app


app = create_app()
