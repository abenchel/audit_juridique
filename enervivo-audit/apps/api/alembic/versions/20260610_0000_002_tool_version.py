"""tool versioning + cache purge flag

Ajoute le suivi de version de l'outil :
  - audits.tool_version      : version courante (config/tool_version.json) au lancement
  - audits.purge_cache       : intention de relance (re-classer tout le projet)
  - classified_documents.tool_version : version qui a produit chaque classification

Migration ADDITIVE (colonnes nullables / avec default) → pas d'impact sur les
lignes existantes (restent NULL / false).

Revision ID: 002
Revises: 001
Create Date: 2026-06-10 00:00:00

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("audits", sa.Column("tool_version", sa.String(20), nullable=True))
    op.add_column(
        "audits",
        sa.Column(
            "purge_cache",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "classified_documents",
        sa.Column("tool_version", sa.String(20), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("classified_documents", "tool_version")
    op.drop_column("audits", "purge_cache")
    op.drop_column("audits", "tool_version")
