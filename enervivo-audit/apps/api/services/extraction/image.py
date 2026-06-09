"""Normalisation d'image avant envoi au LLM vision.

Problème observé sur DIBOS_H : photos smartphone (IMG_xxx.jpg, 5-10 MB en
résolution native 4000x3000) renvoient `Provider returned error 400` côté
OpenRouter/Bedrock. Le rejet est piloté par les DIMENSIONS (cap ~8000 px côté
long), pas seulement par le poids : un PNG rendu par PyMuPDF depuis un scan
300 DPI peut dépasser 8000 px en pesant moins de 4 MB.

Solution : si l'image dépasse le seuil de taille OU de dimensions (_MAX_DIM),
on la recompresse en JPEG ~2048px côté long, qualité 85. Suffisant pour qu'un
LLM vision lise titre/cachets/signatures sur un scan ou une photo de CNI/RIB.
"""

from __future__ import annotations

import io
import logging

_MAX_DIM = 2048  # Claude accepte jusqu'à 8000 px ; 2048 garde les détails (CNI,
# tampons, signatures) sans gonfler la facture. 1568 ancien défaut faisait perdre
# en lisibilité sur les scans 300 DPI.
_MAX_BYTES = 4 * 1024 * 1024  # 4 MB de marge sous le seuil OpenRouter

log = logging.getLogger(__name__)


def normalize_image_for_vision(content: bytes, mime: str) -> tuple[bytes, str]:
    """Renvoie (bytes, mime) prêts à envoyer au LLM vision.

    Si l'image est petite (< 4 MB ET < _MAX_DIM px côté long), on la laisse
    intacte. Sinon on la rouvre via Pillow, downscale et ré-encode en JPEG.
    En cas d'échec Pillow, on renvoie le contenu original (fail-open).

    ⚠️ Le `400` des providers (Bedrock/Claude) est déclenché par les DIMENSIONS
    (cap ~8000 px côté long), pas par le poids. Un PNG rendu par PyMuPDF depuis
    un scan 300 DPI (cas CNI DMONFLANQUIN) peut faire 8000 px tout en pesant
    < 4 MB — il faut donc TOUJOURS vérifier les pixels avant de court-circuiter,
    jamais se fier au seul `len(content)`.
    """
    is_heic = (mime or "").lower() in {"image/heic", "image/heif"}

    try:
        from PIL import Image
    except ImportError:
        log.warning("Pillow absent — image envoyée sans normalisation")
        return content, mime or "image/jpeg"

    # Petit ET non-HEIC : on mesure d'abord les pixels avant de court-circuiter.
    # HEIC est toujours ré-encodé (rejeté par certains providers).
    if len(content) <= _MAX_BYTES and not is_heic:
        try:
            with Image.open(io.BytesIO(content)) as probe:
                if max(probe.size) <= _MAX_DIM:
                    return content, mime or "image/jpeg"  # vraiment petit → intact
        except Exception:  # noqa: BLE001
            return content, mime or "image/jpeg"  # illisible → fail-open
        # sinon : trop de pixels malgré le faible poids → on tombe dans le ré-encode

    try:
        img = Image.open(io.BytesIO(content))
        img.load()
        # Strip EXIF / convert palette/CMYK → RGB pour JPEG
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        # Auto-orient via EXIF (sinon les photos portrait sont à plat)
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception:  # noqa: BLE001
            pass
        w, h = img.size
        if max(w, h) > _MAX_DIM:
            img.thumbnail((_MAX_DIM, _MAX_DIM))
        out = io.BytesIO()
        img.save(out, format="JPEG", quality=85, optimize=True)
        return out.getvalue(), "image/jpeg"
    except Exception as e:  # noqa: BLE001
        log.warning("Échec normalisation image (%s) — envoi brut", e)
        return content, mime or "image/jpeg"
