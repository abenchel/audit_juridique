"""Seed manuel : insère les projets définis dans config/projects_seed.json.

Idempotent : upsert par code projet.

Usage (dans le conteneur api) :
    python -m scripts.seed
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from db.repositories.projects import upsert_project
from db.session import AsyncSessionLocal

SEED_FILE = Path(__file__).parent.parent / "config" / "projects_seed.json"


async def seed() -> None:
    if not SEED_FILE.exists():
        print(f"❌ Fichier seed introuvable : {SEED_FILE}", file=sys.stderr)
        sys.exit(1)

    projects = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    async with AsyncSessionLocal() as session:
        for p in projects:
            await upsert_project(session, p)
            print(f"  ✓ {p['code']:>12} — {p['name']}")
        await session.commit()
    print(f"\n✓ {len(projects)} projets insérés/mis à jour.")


if __name__ == "__main__":
    asyncio.run(seed())
