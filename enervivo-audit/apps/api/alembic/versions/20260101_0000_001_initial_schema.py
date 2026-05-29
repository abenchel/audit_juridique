"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-01-01 00:00:00

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(200), nullable=False, unique=True),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("last_login_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "projects",
        sa.Column("code", sa.String(20), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("sharepoint_url", sa.Text, nullable=False),
        sa.Column("current_jalon", sa.String(20), nullable=True),
        sa.Column("power_mwc", sa.Float, nullable=True),
        sa.Column("department", sa.String(100), nullable=True),
        sa.Column("project_metadata", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "audits",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "project_code",
            sa.String(20),
            sa.ForeignKey("projects.code", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("audit_type", sa.String(50), nullable=False),
        sa.Column("jalons", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("started_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime, nullable=True),
        sa.Column("total_expected", sa.Integer, nullable=True),
        sa.Column("total_found", sa.Integer, nullable=True),
        sa.Column("total_ambiguous", sa.Integer, nullable=True),
        sa.Column("total_missing", sa.Integer, nullable=True),
        sa.Column("result", postgresql.JSONB, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column(
            "triggered_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("ix_audits_project_code", "audits", ["project_code"])
    op.create_index("ix_audits_status", "audits", ["status"])

    op.create_table(
        "classified_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "audit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("audits.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sharepoint_url", sa.Text, nullable=False),
        sa.Column("sharepoint_path", sa.Text, nullable=False),
        sa.Column("file_name", sa.Text, nullable=False),
        sa.Column("file_size", sa.Integer, nullable=False),
        sa.Column("file_hash", sa.String(64), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("classified_type", sa.String(200), nullable=True),
        sa.Column("confidence", sa.Integer, nullable=True),
        sa.Column("reason", sa.Text, nullable=True),
        sa.Column("expected_doc_code", sa.String(120), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("jalon", sa.String(20), nullable=True),
        sa.Column("llm_model", sa.String(120), nullable=True),
        sa.Column("classified_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "confidence IS NULL OR (confidence BETWEEN 0 AND 100)",
            name="check_confidence",
        ),
    )
    op.create_index("ix_classified_documents_audit_id", "classified_documents", ["audit_id"])
    op.create_index("ix_classified_documents_file_hash", "classified_documents", ["file_hash"])
    op.create_index(
        "idx_classified_hash_type",
        "classified_documents",
        ["file_hash", "classified_type"],
    )


def downgrade() -> None:
    op.drop_table("classified_documents")
    op.drop_table("audits")
    op.drop_table("projects")
    op.drop_table("users")
