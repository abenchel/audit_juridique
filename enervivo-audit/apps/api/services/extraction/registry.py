"""Dispatch extracteurs par mime type."""

from __future__ import annotations

from .base import ExtractionError, TextExtractor, truncate_sample
from .csv import CsvExtractor
from .docx import DocxExtractor
from .email import EmailExtractor
from .pdf import PDFExtractor
from .pptx import PptxExtractor
from .text import PlainTextExtractor
from .xlsb import XlsbExtractor
from .xlsx import XlsxExtractor

_PDF = PDFExtractor()
_DOCX = DocxExtractor()
_PPTX = PptxExtractor()
_XLSX = XlsxExtractor()
_XLSB = XlsbExtractor()
_EMAIL = EmailExtractor()
_CSV = CsvExtractor()
_TEXT = PlainTextExtractor()

_MIME_MAP: dict[str, TextExtractor] = {
    "application/pdf": _PDF,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": _DOCX,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template": _DOCX,
    "application/msword": _DOCX,
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": _PPTX,
    "application/vnd.ms-powerpoint": _PPTX,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": _XLSX,
    # .xlsm — Excel macros (openpyxl gère ce format nativement, identique à .xlsx)
    "application/vnd.ms-excel.sheet.macroEnabled.12": _XLSX,
    "application/vnd.ms-excel.sheet.macroenabled.12": _XLSX,
    "application/vnd.ms-excel": _XLSX,
    "message/rfc822": _EMAIL,
    "application/vnd.ms-outlook": _EMAIL,
    "text/csv": _CSV,
    "text/plain": _TEXT,
    "text/xml": _TEXT,
    "application/xml": _TEXT,
}

# Extensions de fallback quand le mime renvoyé par SharePoint est générique
# (application/octet-stream).
_EXT_MAP: dict[str, TextExtractor] = {
    ".pdf": _PDF,
    ".docx": _DOCX,
    ".doc": _DOCX,
    ".dotx": _DOCX,  # template Word, même format OOXML que .docx
    ".pptx": _PPTX,
    ".ppt": _PPTX,
    ".xlsx": _XLSX,
    ".xlsm": _XLSX,  # openpyxl supporte les fichiers Excel macros
    ".xlsb": _XLSB,  # format binaire BIFF12 — extracteur dédié pyxlsb
    ".xls": _XLSX,
    ".eml": _EMAIL,
    ".msg": _EMAIL,
    ".csv": _CSV,
    ".txt": _TEXT,
    ".xml": _TEXT,
}

# Extensions qui doivent IGNORER le mime renvoyé par SharePoint et forcer
# l'extracteur par extension. Exemple typique : Graph renvoie souvent
# `application/vnd.ms-excel` pour un .csv → on l'envoie à openpyxl qui plante
# avec "File is not a zip file". L'extension est plus fiable ici.
_EXT_OVERRIDE: frozenset[str] = frozenset({".csv", ".txt", ".xml", ".xlsb"})

# Mimes images supportés par les modèles vision via OpenRouter (jpeg/png/webp/gif).
# heic/tiff sont parfois non supportés selon le modèle — on les inclut et le LLM
# renverra une erreur si rejetés (catché par l'engine).
IMAGE_MIMES: frozenset[str] = frozenset({
    "image/jpeg", "image/jpg", "image/png", "image/webp",
    "image/gif", "image/tiff", "image/heic", "image/bmp",
})
IMAGE_EXTENSIONS: frozenset[str] = frozenset({
    ".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff", ".heic", ".bmp",
})


def get_extractor(mime_type: str, file_name: str | None = None) -> TextExtractor | None:
    """Cherche l'extracteur par mime, fallback sur l'extension du nom.

    Override : certaines extensions (.csv, .txt, .xml) sont prioritaires sur
    le mime car SharePoint Graph renvoie parfois un mime générique faux
    (ex. `application/vnd.ms-excel` pour un .csv) qui ferait planter l'extracteur.
    """
    name_low = (file_name or "").lower()
    for ext in _EXT_OVERRIDE:
        if name_low.endswith(ext):
            return _EXT_MAP.get(ext)

    ext_map_hit = _MIME_MAP.get(mime_type)
    if ext_map_hit is not None:
        return ext_map_hit
    if name_low:
        for ext, extractor in _EXT_MAP.items():
            if name_low.endswith(ext):
                return extractor
    return None


def is_image(mime_type: str, file_name: str | None = None) -> bool:
    if mime_type and mime_type.lower() in IMAGE_MIMES:
        return True
    if file_name:
        name_low = file_name.lower()
        return any(name_low.endswith(e) for e in IMAGE_EXTENSIONS)
    return False


def extract_text(content: bytes, mime_type: str, file_name: str | None = None) -> str:
    """Extrait + tronque (head + tail)."""
    extractor = get_extractor(mime_type, file_name)
    if extractor is None:
        raise ExtractionError(f"Type non supporté : {mime_type}")
    raw = extractor.extract(content)
    return truncate_sample(raw)
