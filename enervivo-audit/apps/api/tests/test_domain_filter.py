"""Tests filtre domaine @enervivo.fr."""

from __future__ import annotations

import pytest

from services.auth.domain_filter import assert_allowed_email, is_allowed_email


@pytest.mark.parametrize(
    "email,expected",
    [
        ("vincent@enervivo.fr", True),
        ("Vincent@EnerVivo.fr", True),
        ("  pascal@enervivo.fr  ", True),
        ("attacker@evil.com", False),
        ("vincent@enervivo.com", False),
        ("vincent@subenervivo.fr", False),
        ("vincent", False),
        ("", False),
        (None, False),
    ],
)
def test_is_allowed_email(email: str | None, expected: bool) -> None:
    assert is_allowed_email(email) is expected


def test_assert_raises_for_external_domain() -> None:
    with pytest.raises(PermissionError, match="domaine requis"):
        assert_allowed_email("hacker@evil.com")


def test_assert_normalizes_email() -> None:
    assert assert_allowed_email("  Vincent@EnerVivo.fr  ") == "vincent@enervivo.fr"
