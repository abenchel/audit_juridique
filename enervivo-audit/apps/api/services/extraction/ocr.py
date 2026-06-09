"""OCR des PDF scannés via Tesseract — complément de la classification vision.

Contexte : quand un PDF n'a pas de couche texte (`ScanNoTextError`), l'engine
bascule sur une classification multimodale. Avant, seules la 1ʳᵉ et la dernière
page étaient envoyées à Claude en image (cf. `pdf._VISION_PAGES`), donc le
contenu des pages du milieu d'un acte/PV scanné était invisible.

Ce module ajoute une couche OCR : on rend chaque page (jusqu'à `max_pages`) en
image et on en extrait le texte via Tesseract (langue fra+eng). Ce texte est
ensuite **joint au prompt vision** (texte OCR + image page 1) pour que le LLM
ait à la fois le contenu textuel de tout le document ET le visuel
(cachets, signatures, mise en page) que l'OCR aplatit.

⚠️ Périmètre : utilisé **uniquement** pour les PDF scannés, jamais pour les
images natives (.jpg/.png/.heic d'une CNI ou d'un RIB, qui tiennent en une page
et n'ont rien à gagner d'un OCR).

⚠️ Dépendances : `pytesseract` (Python) + le binaire système `tesseract-ocr`
(+ `tesseract-ocr-fra`), installés dans l'image Docker. **Fail-open total** :
si le binaire est absent, si Pillow/pymupdf plante, ou si une page est
illisible → on renvoie `""` (ou ce qui a pu être lu). L'image reste envoyée à
Claude, donc le comportement actuel (vision seule) demeure le plancher.
"""

from __future__ import annotations

import io
import logging

# DPI de rendu pour l'OCR : 200 donne un bon compromis lisibilité Tesseract /
# vitesse (150 est un peu juste pour les petits caractères des actes notariés).
_OCR_DPI = 200
# Plafond de pages OCR-isées : au-delà, on s'arrête (un scan de 200 pages
# bloquerait un slot worker plusieurs minutes — cf. décision SESSION.md).
_DEFAULT_MAX_PAGES = 15
# Langues Tesseract. fra en premier (corpus juridique FR), eng en secours
# (annexes techniques, datasheets). Nécessite tesseract-ocr-fra installé.
_OCR_LANGS = "fra+eng"
# Borne du texte OCR renvoyé : un acte de 15 pages ≈ 30-45k chars. On tronque
# pour ne pas exploser le prompt LLM (le LLM a aussi l'image en complément).
_MAX_OCR_CHARS = 12000
# Seuil minimal de pages pour déclencher l'OCR. Un scan de 1-2 pages (CNI, RIB,
# attestation) a déjà ses 2 pages envoyées en image (page 1 + dernière = tout le
# doc) → l'OCR n'apporte rien et coûterait du CPU. L'OCR ne sert que lorsqu'il y
# a des pages du MILIEU non jointes en image, donc à partir de 3 pages.
_MIN_PAGES_FOR_OCR = 3

log = logging.getLogger(__name__)


def ocr_pdf_pages(content: bytes, max_pages: int = _DEFAULT_MAX_PAGES) -> str:
    """Extrait le texte d'un PDF scanné via Tesseract, page par page.

    Renvoie le texte concaténé (pages séparées par un marqueur), tronqué à
    `_MAX_OCR_CHARS`. Renvoie `""` (pas d'OCR) si le PDF a moins de
    `_MIN_PAGES_FOR_OCR` pages — les 2 pages d'un scan court sont déjà jointes
    en image. Fail-open : renvoie `""` si l'OCR est indisponible ou échoue
    entièrement ; renvoie le texte partiel si seules certaines pages ont pu
    être lues.
    """
    try:
        import pymupdf  # rendu PDF → image
        import pytesseract  # binding Tesseract
        from PIL import Image
    except ImportError as e:
        log.warning("OCR indisponible (dépendance absente : %s) — vision seule", e)
        return ""

    chunks: list[str] = []
    total_chars = 0
    try:
        with pymupdf.open(stream=content, filetype="pdf") as doc:
            if len(doc) < _MIN_PAGES_FOR_OCR:
                # Scan court (1-2 p.) : pages déjà couvertes par les images → skip
                return ""
            n = min(len(doc), max_pages)
            for idx in range(n):
                if total_chars >= _MAX_OCR_CHARS:
                    break
                try:
                    pix = doc[idx].get_pixmap(dpi=_OCR_DPI)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = pytesseract.image_to_string(img, lang=_OCR_LANGS) or ""
                except Exception as pe:  # noqa: BLE001
                    # Page illisible / langue manquante / Tesseract absent du PATH.
                    # On loggue une fois et on continue les autres pages.
                    log.warning("OCR page %d échec (%s)", idx, pe)
                    continue
                text = text.strip()
                if text:
                    chunks.append(f"--- page {idx + 1} ---\n{text}")
                    total_chars += len(text)
    except Exception as e:  # noqa: BLE001
        log.warning("OCR PDF échec global (%s) — vision seule", e)
        return ""

    joined = "\n\n".join(chunks).strip()
    if len(joined) > _MAX_OCR_CHARS:
        joined = joined[:_MAX_OCR_CHARS] + "\n\n[...texte OCR tronqué...]"
    return joined
