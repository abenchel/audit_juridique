"""DTOs project."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ProjectOut(BaseModel):
    code: str
    name: str
    type: str
    sharepoint_url: str
    current_jalon: str | None = None
    power_mwc: float | None = None
    department: str | None = None
    created_at: datetime
    updated_at: datetime


class ProjectSummary(BaseModel):
    code: str
    name: str
    type: str
    current_jalon: str | None
