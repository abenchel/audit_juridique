"""Router auth — endpoint /me et helpers dev."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from services.auth.deps import get_current_user
from services.auth.jwt_verify import TokenPayload

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def me(user: Annotated[TokenPayload, Depends(get_current_user)]) -> dict:
    return {
        "email": user.email,
        "name": user.name,
        "role": user.role,
    }
