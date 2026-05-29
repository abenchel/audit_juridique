"""Extraction XLSB (Excel binaire) via pyxlsb.

openpyxl ne supporte PAS .xlsb (format binaire Microsoft différent de l'OOXML).
On utilise pyxlsb (lib pure-python, lecture seule) qui parse le format BIFF12.
Cas typique : anciens TADD EnerVivo exportés en binaire pour rapidité.
"""

from __future__ import annotations

import io

from .base import HEAD_CHARS, ExtractionError, TextExtractor

_HEAD_BUDGET = HEAD_CHARS * 2


class XlsbExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        try:
            from pyxlsb import open_workbook
        except ImportError as e:  # pragma: no cover
            raise ExtractionError(f"pyxlsb absent : {e}") from e

        try:
            wb_ctx = open_workbook(io.BytesIO(content))
        except Exception as e:
            raise ExtractionError(f"pyxlsb error : {e}") from e

        chunks: list[str] = []
        total = 0
        try:
            with wb_ctx as wb:
                for sheet_name in wb.sheets:
                    chunks.append(f"=== {sheet_name} ===")
                    with wb.get_sheet(sheet_name) as sheet:
                        for row in sheet.rows():
                            cells = [
                                str(c.v) for c in row
                                if c.v is not None and str(c.v).strip()
                            ]
                            if cells:
                                line = " | ".join(cells)
                                chunks.append(line)
                                total += len(line)
                                if total >= _HEAD_BUDGET:
                                    break
                    if total >= _HEAD_BUDGET:
                        break
        except Exception as e:
            raise ExtractionError(f"pyxlsb read error : {e}") from e

        text = "\n".join(chunks)
        if not text.strip():
            raise ExtractionError("XLSB vide")
        return text
