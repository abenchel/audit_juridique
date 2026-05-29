"""Service extraction texte — PDF, DOCX, PPTX, XLSX. Images traitées via vision."""

from __future__ import annotations

from .registry import extract_text, get_extractor, is_image

__all__ = ["extract_text", "get_extractor", "is_image"]
