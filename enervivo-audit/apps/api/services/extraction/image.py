"""Normalisation d'image avant envoi au LLM vision.

Problème observé sur DIBOS_H : photos smartphone (IMG_xxx.jpg, 5-10 MB en
résolution native 4000x3000) renvoient `Provider returned error 400` côté
OpenRouter/Bedrock — les modèles Claude/Gemini ont un cap autour de 5 MB par
image et 1568px côté long.

Solution : si l'image dépasse un seuil de taille OU de dimensions, on la
recompresse en JPEG ~1600px côté long, qualité 85. Suffisant pour qu'un LLM
vision lise titre/cachets/signatures sur un scan ou une photo de CNI/RIB.
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

    Si l'image est petite (< 4 MB et < 1568px), on la laisse intacte.
    Sinon on la rouvre via Pillow, downscale et ré-encode en JPEG.
    En cas d'échec Pillow, on renvoie le contenu original (fail-open).
    """
    if len(content) <= _MAX_BYTES:
        # Petit fichier : on tente d'éviter le coût Pillow, sauf si HEIC
        # (rejeté par certains providers — on le convertit toujours)
        if (mime or "").lower() not in {"image/heic", "image/heif"}:
            return content, mime or "image/jpeg"

    try:
        from PIL import Image
    except ImportError:
        log.warning("Pillow absent — image envoyée sans normalisation")
        return content, mime or "image/jpeg"

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
