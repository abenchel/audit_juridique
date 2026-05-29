"""FastAPI dependencies : current_user + require_admin."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import get_settings
from db.repositories.users import upsert_login
from db.session import get_session

from .domain_filter import is_allowed_email
from .jwt_verify import TokenPayload, decode_bearer_token


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    x_user_email: Annotated[str | None, Header()] = None,
    session: AsyncSession = Depends(get_session),
) -> TokenPayload:
    settings = get_settings()

    # Mode dev : autoriser X-User-Email pour tests Postman
    if settings.environment == "development" and x_user_email:
        if not is_allowed_email(x_user_email):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Email hors domaine @enervivo.fr")
        await upsert_login(session, x_user_email, full_name=x_user_email.split("@")[0])
        return TokenPayload(email=x_user_email, name=x_user_email.split("@")[0])

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bearer token requis")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = decode_bearer_token(token)
    except PermissionError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e)) from e

    # Double check filtre domaine
    if not is_allowed_email(payload.email):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Email hors domaine @enervivo.fr")

    await upsert_login(session, payload.email, payload.name)
    return payload


async def require_admin(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Réservé aux administrateurs")
    return user
