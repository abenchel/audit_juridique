"""Router projets."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.repositories import projects as projects_repo
from db.session import get_session
from models.project import ProjectOut, ProjectSummary
from services.auth.deps import get_current_user
from services.auth.jwt_verify import TokenPayload

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectSummary])
async def list_projects(
    _user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> list[ProjectSummary]:
    rows = await projects_repo.list_projects(session)
    return [
        ProjectSummary(code=p.code, name=p.name, type=p.type, current_jalon=p.current_jalon) for p in rows
    ]


@router.get("/{code}", response_model=ProjectOut)
async def get_project(
    code: str,
    _user: Annotated[TokenPayload, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> ProjectOut:
    p = await projects_repo.get_project(session, code)
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Projet {code} introuvable")
    return ProjectOut.model_validate(
        {
            "code": p.code,
            "name": p.name,
            "type": p.type,
            "sharepoint_url": p.sharepoint_url,
            "current_jalon": p.current_jalon,
            "power_mwc": p.power_mwc,
            "department": p.department,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
        }
    )
