"""Provider Anthropic direct — pour switcher depuis OpenRouter.

Stub : implémentation effective via httpx vers https://api.anthropic.com/v1/messages.
"""

from __future__ import annotations

import json
import logging
import re

import httpx

from config.settings import get_settings

from .base import LLMProvider

log = logging.getLogger(__name__)

_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def _parse_json_lenient(text: str) -> dict:
    text = text.strip()
    m = _JSON_FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    return json.loads(text)


class AnthropicDirectProvider(LLMProvider):
    def __init__(self) -> None:
        self._settings = get_settings()
        if not self._settings.anthropic_api_key or not self._settings.anthropic_api_key.get_secret_value():
            log.warning("ANTHROPIC_API_KEY vide — provider direct inutilisable")

    @property
    def model_name(self) -> str:
        # OpenRouter utilise "anthropic/claude-haiku-4-5" — Anthropic direct juste "claude-haiku-4-5"
        model = self._settings.openrouter_default_model
        return model.split("/", 1)[-1] if "/" in model else model

    async def complete_json(
        self, system_prompt: str, user_prompt: str, max_tokens: int = 800
    ) -> dict:
        s = self._settings
        if not s.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY non configuré")

        headers = {
            "x-api-key": s.anthropic_api_key.get_secret_value(),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        body = {
            "model": self.model_name,
            "max_tokens": max_tokens,
            "temperature": 0.0,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }
        async with httpx.AsyncClient(timeout=s.llm_timeout_seconds) as cli:
            r = await cli.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
            r.raise_for_status()
            data = r.json()

        # data["content"] = [{"type": "text", "text": "..."}, ...]
        text = "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
        return _parse_json_lenient(text)
