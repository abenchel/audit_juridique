"""DTOs documents — Pydantic v2."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FileMetadata(BaseModel):
    """Métadonnée fichier SharePoint — sans le contenu binaire."""

    name: str
    path: str  # chemin dans le dossier projet (ex. "/01_Foncier/contrat.pdf")
    url: str  # URL SharePoint cliquable (webUrl)
    size: int
    mime_type: str = "application/octet-stream"
    modified_at: datetime | None = None
    drive_item_id: str | None = None  # Graph API ID


class FileContent(BaseModel):
    """Contenu binaire d'un fichier — en RAM uniquement, jamais persisté."""

    metadata: FileMetadata
    content: bytes = Field(repr=False)


class ClassificationResult(BaseModel):
    type: str
    confidence: int = Field(ge=0, le=100)
    reason: str
