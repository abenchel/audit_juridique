"""Provider OpenRouter — httpx async vers /chat/completions OpenAI-compatible."""

from __future__ import annotations

import base64
import json
import logging
import re

import httpx
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from config.settings import get_settings

from .base import LLMProvider

log = logging.getLogger(__name__)

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


class OpenRouterError(Exception):
    """Erreur appel OpenRouter."""


def _parse_json_lenient(text: str) -> dict:
    """Parse JSON, en strippant un éventuel ```json ... ``` fence."""
    text = text.strip()
    m = _JSON_FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    return json.loads(text)


class OpenRouterProvider(LLMProvider):
    def __init__(self) -> None:
        self._settings = get_settings()
        if not self._settings.openrouter_api_key.get_secret_value():
            log.warning("OPENROUTER_API_KEY vide — les appels LLM échoueront")

    @property
    def model_name(self) -> str:
        return self._settings.openrouter_default_model

    async def _post_chat(
        self,
        user_content: str | list[dict],
        system_prompt: str,
        model: str | None = None,
        max_tokens: int = 800,
    ) -> dict:
        """POST /chat/completions avec retry et parsing JSON. `user_content` peut être
        une string (texte simple) ou une liste de blocs multimodaux (texte + image_url).

        `model` : surcharge optionnelle du modèle (None → openrouter_default_model).
        Sert au split texte/vision (cf. complete_json_vision).
        `max_tokens` : 800 par défaut. 300 (ancien défaut) suffisait pour Haiku mais
        TRONQUE le JSON de Gemini Flash-Lite, dont les `reason` sont plus longues
        (observé sur DIBOS_H : « JSON LLM invalide '{"type": "..." ' » sur ~10
        fichiers). 800 couvre {type,confidence,reason} verbeux. On ne paie que les
        tokens réellement générés, pas le plafond. La passe 2 plans de masse renvoie
        N objets d'un coup → passe une valeur encore plus haute (cf. plan_masse.py).
        valeur plus haute, sinon le JSON est tronqué et le parsing échoue."""
        s = self._settings
        headers = {
            "Authorization": f"Bearer {s.openrouter_api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://audit.enervivo.fr",
            "X-Title": "EnerVivo Audit",
        }
        body = {
            "model": model or s.openrouter_default_model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                    "cache_control": {"type": "ephemeral"},  # ★ OpenRouter prompt caching (5min)
                },
                {"role": "user", "content": user_content},
            ],
            "temperature": 0.0,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"},
        }

        data: dict = {}
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(s.llm_max_retries),
            wait=wait_exponential(multiplier=1, min=2, max=15),
            # Inclut RemoteProtocolError + ConnectError : OpenRouter/Bedrock coupe
            # parfois la connexion sous forte charge → on retry au lieu d'échouer.
            retry=retry_if_exception_type(
                (
                    httpx.HTTPStatusError,
                    httpx.TimeoutException,
                    httpx.RemoteProtocolError,
                    httpx.ConnectError,
                    httpx.ReadError,
                )
            ),
            reraise=True,
        ):
            with attempt:
                async with httpx.AsyncClient(timeout=s.llm_timeout_seconds) as cli:
                    r = await cli.post(
                        f"{s.openrouter_base_url}/chat/completions",
                        headers=headers,
                        json=body,
                    )
                    if r.status_code in {429, 500, 502, 503, 504}:
                        r.raise_for_status()
                    if r.status_code >= 400:
                        raise OpenRouterError(f"OpenRouter {r.status_code} : {r.text[:300]}")
                    data = r.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise OpenRouterError(f"Réponse mal formée : {data}") from e

        try:
            return _parse_json_lenient(content)
        except json.JSONDecodeError as e:
            raise OpenRouterError(f"JSON LLM invalide : {content!r}") from e

    async def complete_json(
        self, system_prompt: str, user_prompt: str, max_tokens: int = 1200
    ) -> dict:
        return await self._post_chat(user_prompt, system_prompt, max_tokens=max_tokens)

    async def complete_json_vision(
        self,
        system_prompt: str,
        user_prompt: str,
        images: list[bytes] | list[tuple[bytes, str]],
    ) -> dict:
        """Multimodal : texte + images inline en data URI base64.

        Format OpenAI-compatible accepté par OpenRouter/Bedrock pour les modèles
        vision (Claude Haiku 4.5, Sonnet, Gemini Flash, etc.).

        `images` peut être :
          - `list[bytes]` (legacy) : PNG bytes, mime déduit "image/png"
          - `list[tuple[bytes, str]]` : (bytes, mime_type) pour supporter jpg/webp/etc.
        """
        content: list[dict] = [{"type": "text", "text": user_prompt}]
        for item in images:
            if isinstance(item, tuple):
                data, mime = item
            else:
                data, mime = item, "image/png"
            # Quelques mimes non supportés par les modèles vision (heic) : convertir
            # côté caller, ici on passe ce qu'on reçoit.
            b64 = base64.b64encode(data).decode("ascii")
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime};base64,{b64}"},
                }
            )
        # Split texte/vision : si openrouter_vision_model est défini, la vision
        # l'utilise ; sinon None → _post_chat retombe sur le modèle par défaut.
        vision_model = self._settings.openrouter_vision_model or None
        return await self._post_chat(content, system_prompt, model=vision_model)
