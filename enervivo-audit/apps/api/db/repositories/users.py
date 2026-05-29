"""Repository utilisateurs."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    res = await session.execute(select(User).where(User.email == email.lower()))
    return res.scalar_one_or_none()


async def upsert_login(session: AsyncSession, email: str, full_name: str) -> User:
    """Crée ou met à jour un user à chaque login (last_login_at)."""
    email = email.lower()
    user = await get_by_email(session, email)
    if user:
        user.last_login_at = datetime.utcnow()
        user.full_name = full_name
        return user
    user = User(
        id=uuid.uuid4(),
        email=email,
        full_name=full_name,
        last_login_at=datetime.utcnow(),
    )
    session.add(user)
    return user
