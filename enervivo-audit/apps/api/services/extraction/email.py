"""Extraction email — .eml (stdlib RFC822) et .msg (extract-msg / Outlook).

Cas d'usage : CR de RDV envoyés par mail (mairie, DDT, Chambre d'Agriculture),
échanges contractuels, AR de dépôt urbanisme, etc.

Structure du sample renvoyé :
    De: ...
    À: ...
    Date: ...
    Objet: ...

    [Corps du mail tronqué]

Les pièces jointes ne sont PAS extraites ici (elles arrivent comme fichiers
séparés via le listing SharePoint quand l'utilisateur les enregistre).
"""

from __future__ import annotations

import email as stdlib_email
import io
from email import policy
from email.parser import BytesParser

from .base import HEAD_CHARS, ExtractionError, TextExtractor

_HEAD_BUDGET = HEAD_CHARS * 2


def _body_from_eml(msg: stdlib_email.message.EmailMessage) -> str:
    """Choisit la meilleure version texte du corps. Préfère text/plain, fallback text/html."""
    # get_body suit RFC compliant : text/plain > text/html
    body = msg.get_body(preferencelist=("plain", "html"))
    if body is None:
        return ""
    try:
        content = body.get_content()
    except Exception:
        return ""
    return content or ""


def _strip_html(s: str) -> str:
    """Strip naïf des tags HTML — pas parfait mais suffisant pour classifier."""
    import re

    s = re.sub(r"<style[^>]*>.*?</style>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<script[^>]*>.*?</script>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _format_header(headers: dict[str, str], body: str) -> str:
    parts = [
        f"De: {headers.get('from', '')}",
        f"À: {headers.get('to', '')}",
        f"Date: {headers.get('date', '')}",
        f"Objet: {headers.get('subject', '')}",
        "",
        body,
    ]
    return "\n".join(parts).strip()


class EmailExtractor(TextExtractor):
    """Détecte .eml (commence par headers RFC822) ou .msg (compound file binaire OLE)."""

    def extract(self, content: bytes) -> str:
        # .msg : signature OLE2 (D0 CF 11 E0 A1 B1 1A E1)
        if content[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
            return self._extract_msg(content)
        # Sinon traité comme .eml RFC822
        return self._extract_eml(content)

    def _extract_eml(self, content: bytes) -> str:
        try:
            msg: stdlib_email.message.EmailMessage = BytesParser(policy=policy.default).parsebytes(content)  # type: ignore[assignment]
        except Exception as e:
            raise ExtractionError(f"EML parse error : {e}") from e

        headers = {
            "from": str(msg.get("From", "") or ""),
            "to": str(msg.get("To", "") or ""),
            "date": str(msg.get("Date", "") or ""),
            "subject": str(msg.get("Subject", "") or ""),
        }
        body = _body_from_eml(msg)
        # Si seulement HTML disponible, strip les tags
        if body and "<" in body and ">" in body:
            body = _strip_html(body)

        text = _format_header(headers, body[:_HEAD_BUDGET])
        if not text.strip() or text.strip() in {"De: ", "Objet:"}:
            raise ExtractionError("EML vide ou illisible")
        return text

    def _extract_msg(self, content: bytes) -> str:
        try:
            import extract_msg  # import paresseux
        except ImportError as e:  # pragma: no cover
            raise ExtractionError(f"extract-msg absent : {e}") from e

        try:
            msg = extract_msg.openMsg(io.BytesIO(content))
        except Exception as e:
            raise ExtractionError(f"MSG parse error : {e}") from e

        try:
            headers = {
                "from": getattr(msg, "sender", "") or "",
                "to": getattr(msg, "to", "") or "",
                "date": str(getattr(msg, "date", "") or ""),
                "subject": getattr(msg, "subject", "") or "",
            }
            body = (getattr(msg, "body", None) or getattr(msg, "htmlBody", None) or "")
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="ignore")
            if body and "<" in body and ">" in body:
                body = _strip_html(body)
        finally:
            try:
                msg.close()
            except Exception:
                pass

        text = _format_header(headers, body[:_HEAD_BUDGET])
        if not text.strip():
            raise ExtractionError("MSG vide ou illisible")
        return text
