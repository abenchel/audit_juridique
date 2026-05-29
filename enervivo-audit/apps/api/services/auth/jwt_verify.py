"""Vérifie le JWT NextAuth côté FastAPI.

NextAuth v5 utilise par défaut JWE chiffré avec une clé dérivée de NEXTAUTH_SECRET.
Côté API, on accepte deux modes :

  1) JWT signé HS256 émis par un endpoint Next.js dédié (recommandé) : le frontend
     appelle /api/auth/token (route serveur Next.js) qui signe un JWT minimal
     {email, name} avec NEXTAUTH_SECRET, puis l'envoie dans Authorization: Bearer.
     Le backend valide via HS256.

  2) Mode développement : header X-User-Email simple (à n'utiliser que si
     ENVIRONMENT=development), pour faciliter les tests Postman.

La validation HS256 est volontairement simple — pas de tentative de déchiffrer
le JWE NextAuth qui changerait à chaque mise à jour du SDK.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr

from config.settings import get_settings


class TokenPayload(BaseModel):
    email: EmailStr
    name: str
    role: str = "user"
    iat: int | None = None
    exp: int | None = None


def decode_bearer_token(token: str) -> TokenPayload:
    """Décode un JWT HS256 signé avec NEXTAUTH_SECRET."""
    settings = get_settings()
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.nextauth_secret.get_secret_value(),
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
    except JWTError as e:
        raise PermissionError(f"JWT invalide : {e}") from e

    if "email" not in payload:
        raise PermissionError("JWT sans email")
    return TokenPayload(**payload)


def issue_test_token(email: str, name: str = "Test User") -> str:
    """Helper dev/test : génère un JWT signé valide 1h. Ne pas exposer en prod."""
    settings = get_settings()
    now = int(datetime.utcnow().timestamp())
    payload = {"email": email, "name": name, "iat": now, "exp": now + 3600}
    return jwt.encode(payload, settings.nextauth_secret.get_secret_value(), algorithm="HS256")
