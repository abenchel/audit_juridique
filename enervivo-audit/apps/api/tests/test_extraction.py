"""Tests extraction de texte."""

from __future__ import annotations

import pytest

from services.extraction.base import ExtractionError, truncate_sample
from services.extraction.registry import extract_text, get_extractor


def test_truncate_short_text_unchanged() -> None:
    assert truncate_sample("hello") == "hello"


def test_truncate_long_text_keeps_head_and_tail() -> None:
    text = "A" * 3000 + "B" * 5000 + "C" * 1000
    out = truncate_sample(text)
    assert out.startswith("A" * 100)
    assert out.endswith("C" * 100)
    assert "[...]" in out


def test_unsupported_mime_raises() -> None:
    with pytest.raises(ExtractionError):
        extract_text(b"data", "image/jpeg")


def test_registry_pdf() -> None:
    assert get_extractor("application/pdf") is not None


def test_registry_unknown() -> None:
    assert get_extractor("application/x-unknown") is None
