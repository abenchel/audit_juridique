"""Router audits — création, consultation, SSE temps réel."""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from db.repositories import audits as audits_repo
from db.repositories import classifications as classifications_repo
from db.repositories import projects as projects_repo
from db.repositories import users as users_repo
from db.session import get_session
from models.audit import AuditCreateRequest, AuditCreateResponse
from services.auth.deps import get_current_user
from services.auth.jwt_verify import TokenPayload
from services.version import current_version, oldest_version

router = APIRouter(prefix="/audits", tags=["audits"])


@router.post("", response_model=AuditCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_audit(
    body: AuditCreateRequest,
    user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> AuditCreateResponse:
    project = await projects_repo.get_project(session, body.project_code)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Projet {body.project_code} introuvable")

    db_user = await users_repo.get_by_email(session, user.email)

    # Relance « + nettoyer le cache » : on purge les classifications du projet
    # AVANT de créer le nouvel audit (qui n'en a pas encore → pas de conflit).
    # Le bypass du cache global est assuré par purge_cache=True côté engine.
    if body.purge_cache:
        await classifications_repo.purge_for_project(session, body.project_code)

    audit = await audits_repo.create_audit(
        session,
        project_code=body.project_code,
        audit_type=body.audit_type,
        jalons=body.jalons or [project.current_jalon] if project.current_jalon else body.jalons,
        status="pending",
        triggered_by=db_user.id if db_user else None,
        # Versioning : on fige la version courante de l'outil au lancement.
        tool_version=current_version(),
        purge_cache=body.purge_cache,
    )
    await session.commit()

    # Push Celery task
    from tasks.audit_tasks import run_audit_task

    run_audit_task.delay(str(audit.id))

    return AuditCreateResponse(id=str(audit.id), status="pending")


@router.get("/{audit_id}")
async def get_audit(
    audit_id: uuid.UUID,
    _user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    audit = await audits_repo.get_audit(session, audit_id)
    if not audit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Audit introuvable")

    # Progression live (utilisée par AuditProgress pour reconstruire l'état au refresh)
    progress_total: int | None = None
    progress_done: int | None = None
    progress_current_file: str | None = None
    if audit.status in {"pending", "running"}:
        # Snapshots Redis (TTL 24h) posés par engine.py au fil de l'audit
        try:
            from redis.asyncio import Redis

            from config.settings import get_settings

            _s = get_settings()
            _r = Redis.from_url(_s.redis_url, decode_responses=True)
            _t = await _r.get(f"audit:{audit_id}:total")
            _d = await _r.get(f"audit:{audit_id}:done")
            _cf = await _r.get(f"audit:{audit_id}:current_file")
            await _r.close()
            if _t is not None:
                progress_total = int(_t)
            if _d is not None:
                progress_done = int(_d)
            progress_current_file = _cf
        except Exception:
            pass

    return {
        "id": str(audit.id),
        "project_code": audit.project_code,
        "audit_type": audit.audit_type,
        "status": audit.status,
        "started_at": audit.started_at,
        "completed_at": audit.completed_at,
        "jalons": audit.jalons,
        "total_expected": audit.total_expected,
        "total_found": audit.total_found,
        "total_ambiguous": audit.total_ambiguous,
        "total_missing": audit.total_missing,
        "result": audit.result,
        "error_message": audit.error_message,
        # Snapshot progression pour la page audit (refresh-friendly)
        "progress_total": progress_total,
        "progress_done": progress_done,
        "progress_current_file": progress_current_file,
    }


@router.post("/{audit_id}/cancel", status_code=status.HTTP_202_ACCEPTED)
async def cancel_audit(
    audit_id: uuid.UUID,
    _user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Annule un audit en cours.

    Stratégie : (1) pose un flag Redis `audit:{id}:cancel` que le worker check
    à chaque fichier → arrêt propre dans ~5s. (2) marque immédiatement le
    status DB en 'failed' pour libérer l'UI. Le worker, en voyant le flag,
    skippe le reste et n'écrasera pas le status.
    """
    audit = await audits_repo.get_audit(session, audit_id)
    if not audit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Audit introuvable")
    if audit.status not in {"pending", "running"}:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Audit déjà terminé (status={audit.status}), rien à annuler",
        )

    # Flag Redis (TTL 1h) — lu par engine._wrapped à chaque itération
    try:
        from redis.asyncio import Redis

        from config.settings import get_settings

        s = get_settings()
        r = Redis.from_url(s.redis_url, decode_responses=True)
        await r.set(f"audit:{audit_id}:cancel", "1", ex=3600)
        await r.close()
    except Exception:
        # Si Redis KO, on continue quand même — au moins le status DB sera mis à jour
        pass

    audit.status = "failed"
    audit.error_message = "annulé par l'utilisateur"
    from datetime import datetime

    audit.completed_at = datetime.utcnow()
    await session.commit()

    return {"id": str(audit.id), "status": "failed", "cancelled": True}


@router.delete("/{audit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_audit(
    audit_id: uuid.UUID,
    _user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> None:
    audit = await audits_repo.get_audit(session, audit_id)
    if not audit:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Audit introuvable")
    if audit.status in {"pending", "running"}:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Impossible de supprimer un audit en cours — annule-le d'abord",
        )
    await session.delete(audit)
    await session.commit()


@router.get("/{audit_id}/stream")
async def stream_audit(
    audit_id: uuid.UUID,
    token: Annotated[str | None, Query()] = None,
):
    # EventSource ne supporte pas les headers — on accepte le JWT via ?token=
    from services.auth.domain_filter import is_allowed_email
    from services.auth.jwt_verify import decode_bearer_token

    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token requis (query param ?token=)")
    try:
        payload = decode_bearer_token(token)
    except PermissionError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e)) from e
    if not is_allowed_email(payload.email):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Email hors domaine @enervivo.fr")
    """SSE temps réel — Redis pub-sub channel `audit:{id}`."""
    from redis.asyncio import Redis

    from config.settings import get_settings

    s = get_settings()

    async def event_generator():
        redis = Redis.from_url(s.redis_url, decode_responses=True)
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"audit:{audit_id}")
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    data = message["data"]
                    yield {"event": "audit", "data": data}
                    try:
                        payload = json.loads(data)
                        if payload.get("event") in ("completed", "failed"):
                            break
                    except json.JSONDecodeError:
                        pass
        finally:
            await pubsub.unsubscribe(f"audit:{audit_id}")
            await pubsub.close()
            await redis.close()

    return EventSourceResponse(event_generator())


@router.get("/project/{project_code}")
async def list_audits_for_project(
    project_code: str,
    _user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> list[dict[str, Any]]:
    audits = await audits_repo.list_audits_for_project(session, project_code)
    # Versions du cache : agrège les tool_version des classifs de chaque audit
    # en une requête (évite le N+1) → "version du cache" = la plus ancienne.
    versions_map = await classifications_repo.tool_versions_by_audit(
        session, [a.id for a in audits]
    )
    return [
        {
            "id": str(a.id),
            "audit_type": a.audit_type,
            "status": a.status,
            "started_at": a.started_at,
            "completed_at": a.completed_at,
            "total_expected": a.total_expected,
            "total_found": a.total_found,
            "total_ambiguous": a.total_ambiguous,
            "total_missing": a.total_missing,
            "tool_version": a.tool_version,
            "cache_version": oldest_version(versions_map.get(a.id, [])),
        }
        for a in audits
    ]
