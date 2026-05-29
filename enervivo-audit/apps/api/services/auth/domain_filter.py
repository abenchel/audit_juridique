"""Filtre strict domaine email — défense en profondeur.

NextAuth filtre déjà côté frontend, mais on re-vérifie côté API : si un attaquant
crée un JWT signé valide avec un email externe, on rejette ici.
"""

from __future__ import annotations

from config.settings import get_settings


def is_allowed_email(email: str | None) -> bool:
    if not email:
        return False
    settings = get_settings()
    return email.strip().lower().endswith(f"@{settings.allowed_email_domain.lower()}")


def assert_allowed_email(email: str | None) -> str:
    if not is_allowed_email(email):
        raise PermissionError(f"Email non autorisé (domaine requis : @{get_settings().allowed_email_domain})")
    assert email is not None
    return email.strip().lower()
