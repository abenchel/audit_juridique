"""Schéma SQLAlchemy 2.0 — EnerVivo Audit.

Tables :
  - users          : identités Entra ID (pas de mdp ; auth via JWT NextAuth)
  - projects       : projets PV (code, type, URL SharePoint, jalon courant)
  - audits         : audits lancés (statut, totaux, rapport JSONB complet)
  - classified_documents : documents identifiés (cache cross-audit par hash)

Principe : AUCUN fichier n'est stocké en DB. Seules métadonnées + rapport JSONB.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import ARRAY, CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _utcnow() -> datetime:
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(20), default="user")  # 'user' | 'admin'
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)


class Project(Base):
    __tablename__ = "projects"

    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(50))  # 'AgriPV' | 'S21'
    sharepoint_url: Mapped[str] = mapped_column(Text)
    current_jalon: Mapped[str | None] = mapped_column(String(20), nullable=True)
    power_mwc: Mapped[float | None] = mapped_column(Float, nullable=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    project_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow)

    audits: Mapped[list[Audit]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Audit(Base):
    __tablename__ = "audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_code: Mapped[str] = mapped_column(ForeignKey("projects.code", ondelete="CASCADE"), index=True)
    audit_type: Mapped[str] = mapped_column(String(50))  # 'juridique' | 'technique' | 'financier'
    jalons: Mapped[list[str]] = mapped_column(ARRAY(String))
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    # 'pending' | 'running' | 'completed' | 'failed'

    started_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    total_expected: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_found: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_ambiguous: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_missing: Mapped[int | None] = mapped_column(Integer, nullable=True)

    result: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    triggered_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    project: Mapped[Project] = relationship(back_populates="audits")
    documents: Mapped[list[ClassifiedDocument]] = relationship(
        back_populates="audit", cascade="all, delete-orphan"
    )


class ClassifiedDocument(Base):
    __tablename__ = "classified_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("audits.id", ondelete="CASCADE"), index=True)

    sharepoint_url: Mapped[str] = mapped_column(Text)  # URL cliquable
    sharepoint_path: Mapped[str] = mapped_column(Text)
    file_name: Mapped[str] = mapped_column(Text)
    file_size: Mapped[int] = mapped_column(Integer)
    file_hash: Mapped[str] = mapped_column(String(64), index=True)  # SHA-256 → cache cross-audit
    mime_type: Mapped[str] = mapped_column(String(100))

    classified_type: Mapped[str | None] = mapped_column(String(200), nullable=True)
    confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    expected_doc_code: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(20))
    # 'present' | 'ambiguous' | 'missing' | 'other' | 'error' | 'not_applicable'

    jalon: Mapped[str | None] = mapped_column(String(20), nullable=True)
    llm_model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    classified_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow)

    audit: Mapped[Audit] = relationship(back_populates="documents")

    __table_args__ = (
        CheckConstraint("confidence IS NULL OR (confidence BETWEEN 0 AND 100)", name="check_confidence"),
        Index("idx_classified_hash_type", "file_hash", "classified_type"),
    )
