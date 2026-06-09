"""Interface LLMProvider — abstrait OpenRouter / Anthropic direct."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def complete_json(
        self, system_prompt: str, user_prompt: str, max_tokens: int = 800
    ) -> dict:
        """Appelle le LLM et retourne le JSON parsé.

        Doit gérer : timeout, retries 3x exponentiel sur 429/5xx, parsing JSON
        avec tolérance markdown fence ```json``` autour.

        `max_tokens` : 300 par défaut (suffit pour classer un fichier). Les
        appels qui renvoient plusieurs objets (passe 2 plans de masse) doivent
        passer une valeur plus haute pour éviter un JSON tronqué.
        """
        raise NotImplementedError

    async def complete_json_vision(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[bytes] | list[tuple[bytes, str]],
    ) -> dict:
        """Appelle le LLM en mode multimodal (texte + images inline base64).

        `images` peut être `list[bytes]` (mime image/png par défaut) ou
        `list[tuple[bytes, mime_type]]` pour supporter jpg/webp/png.

        Default : NotImplementedError. Les providers qui supportent la vision
        (OpenRouter sur Claude/Gemini, etc.) doivent surcharger cette méthode.
        """
        raise NotImplementedError("Vision non supportée par ce provider")

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Identifie le modèle utilisé (pour logging/audit)."""
        raise NotImplementedError
