"""Stub OCR — sera implémenté en v2 si la volumétrie de scans justifie pytesseract."""

from __future__ import annotations

from .base import ExtractionError, TextExtractor


class OCRExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        raise ExtractionError("OCR non implémenté (v2 — pytesseract)")
