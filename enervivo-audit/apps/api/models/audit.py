"""DTOs audit (Pydantic v2) — shape du JSONB result."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

AuditStatus = Literal["pending", "running", "completed", "failed"]
DocumentStatus = Literal["present", "ambiguous", "missing", "other", "error", "not_applicable"]


class FoundFile(BaseModel):
    file_name: str
    sharepoint_url: str
    sharepoint_path: str
    confidence: int = Field(ge=0, le=100)
    reason: str
    file_hash: str | None = None


class ExpectedDocument(BaseModel):
    code: str
    name: str
    propriete: str  # 'Obligatoire' | 'Facultatif' | 'Cas par cas' | 'Annexes 3 PDB' | 'Informatif'
    status: DocumentStatus
    found_files: list[FoundFile] = Field(default_factory=list)
    note: str | None = None


class JalonReport(BaseModel):
    jalon: str
    total_expected: int
    total_present: int
    total_ambiguous: int
    total_missing: int
    completion_pct: int
    documents: list[ExpectedDocument]


class UnclassifiedFile(BaseModel):
    file_name: str
    sharepoint_url: str
    sharepoint_path: str
    classified_type: str | None
    confidence: int | None
    reason: str | None


class ErrorFile(BaseModel):
    file_name: str
    sharepoint_url: str
    sharepoint_path: str
    error: str


class IgnoredFile(BaseModel):
    """Fichier sciemment ignoré au listing (vidéo, image, pptx, etc.).
    Pas un échec — c'est juste un type qu'on ne sait pas (ou ne veut pas)
    classifier dans l'audit juridique."""

    file_name: str
    sharepoint_url: str
    sharepoint_path: str
    mime_type: str
    size: int
    reason: str  # ex: "video", "presentation", "spreadsheet", "image"


class AuditReport(BaseModel):
    audit_id: str
    project_code: str
    project_name: str
    project_type: str
    audit_type: str
    jalons_audited: list[str]
    started_at: datetime
    completed_at: datetime | None
    model_used: str | None

    total_files_scanned: int
    total_expected: int
    total_present: int
    total_ambiguous: int
    total_missing: int
    overall_completion_pct: int

    top_critical_missing: list[str] = Field(default_factory=list)
    jalons: list[JalonReport]
    unclassified: list[UnclassifiedFile]
    errors: list[ErrorFile]
    # Fichiers SharePoint sciemment écartés au listing (vidéos, images, pptx…).
    # Default vide pour rétro-compat avec les anciens rapports JSONB en DB.
    ignored: list[IgnoredFile] = Field(default_factory=list)


class AuditCreateRequest(BaseModel):
    project_code: str
    audit_type: Literal["juridique", "technique", "financier"] = "juridique"
    jalons: list[str] = Field(default_factory=list)  # vide = tous les jalons attendus du projet


class AuditCreateResponse(BaseModel):
    id: str
    status: AuditStatus
