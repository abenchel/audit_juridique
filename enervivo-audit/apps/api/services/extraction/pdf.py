"""Extraction PDF via pdfplumber — **lazy** (head + tail uniquement).

Stratégie : on lit les premières pages jusqu'à atteindre `HEAD_CHARS * 2`
de texte, puis on saute aux 3 dernières pages pour la "tail". On évite ainsi
de décompresser tout le contenu d'un PDF de 200 pages (PADD, PLU…) pour ne
garder au final que 2800 chars (head 2000 + tail 800) via `truncate_sample`.

Gain RAM : ~10-20× sur les gros PDFs. Gain temps : ~5-10× sur les gros PDFs.
Risque acceptable : 1-2 % des docs où le titre/signataire est en plein milieu.

Tolérance : si pdfplumber échoue (PDF scanné sans OCR, corrompu), lève
ExtractionError — l'audit marquera le doc en statut 'error'.
"""

from __future__ import annotations

import io

import pdfplumber

from .base import HEAD_CHARS, ExtractionError, ScanNoTextError, TextExtractor

# Marge de sécurité : on lit jusqu'à 2× HEAD_CHARS de texte avant de stopper
# (les pages 1-2 sont souvent une page de garde quasi-vide, donc on a besoin
# d'aller chercher un peu plus loin pour assurer 2000 chars utiles).
_HEAD_BUDGET = HEAD_CHARS * 2
# Nombre de dernières pages à lire pour la tail (signatures, dates, annexes).
_TAIL_PAGES = 3


class PDFExtractor(TextExtractor):
    def extract(self, content: bytes) -> str:
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                n_pages = len(pdf.pages)

                # --- HEAD : lit les pages depuis le début jusqu'à _HEAD_BUDGET chars ---
                head_chunks: list[str] = []
                head_len = 0
                pages_read = 0
                for i, page in enumerate(pdf.pages):
                    t = page.extract_text() or ""
                    if t.strip():
                        head_chunks.append(t)
                        head_len += len(t)
                    pages_read = i + 1
                    if head_len >= _HEAD_BUDGET:
                        break

                head_text = "\n\n".join(head_chunks)

                # --- TAIL : dernières pages, seulement si on n'a pas déjà tout lu ---
                tail_start = max(pages_read, n_pages - _TAIL_PAGES)
                tail_chunks: list[str] = []
                if tail_start < n_pages:
                    for j in range(tail_start, n_pages):
                        t = pdf.pages[j].extract_text() or ""
                        if t.strip():
                            tail_chunks.append(t)
                tail_text = "\n\n".join(tail_chunks)
        except ExtractionError:
            raise
        except Exception as e:
            raise ExtractionError(f"pdfplumber error : {e}") from e

        if not head_text.strip() and not tail_text.strip():
            # Vraie absence de couche texte → l'engine basculera sur le LLM vision
            # (rendering des pages 1 + dernière via pymupdf, classification multimodal).
            raise ScanNoTextError("PDF sans couche texte (scan)")

        if tail_text and tail_start > pages_read:
            return head_text + "\n\n[...pages intermédiaires omises...]\n\n" + tail_text
        return head_text + ("\n\n" + tail_text if tail_text else "")


# Pages rendues pour le fallback vision : DPI 150 = lisible mais < 200 KB / page typique.
_VISION_DPI = 150
# Indices des pages à rendre quand un scan est détecté (page 1 + dernière).
# Si le PDF n'a qu'une page, on n'en renvoie qu'une.
_VISION_PAGES = (0, -1)


def render_pdf_pages_to_png(content: bytes, page_indices: tuple[int, ...] = _VISION_PAGES) -> list[bytes]:
    """Rend les pages indiquées d'un PDF en PNG inline (pour fallback vision LLM).

    Utilisé quand pdfplumber lève `ScanNoTextError` : on bascule sur une
    classification multimodale (image + filename) via le LLM.
    """
    import pymupdf  # import paresseux : seuls les PDF scannés en ont besoin

    pngs: list[bytes] = []
    with pymupdf.open(stream=content, filetype="pdf") as doc:
        n = len(doc)
        if n == 0:
            return []
        # Dédoublonne les indices résolus (0 et -1 pour un PDF 1 page = même page)
        resolved = sorted({(i if i >= 0 else n + i) for i in page_indices if -n <= i < n})
        for idx in resolved:
            pix = doc[idx].get_pixmap(dpi=_VISION_DPI)
            pngs.append(pix.tobytes("png"))
    return pngs
