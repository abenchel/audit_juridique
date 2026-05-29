"""Service LLM — abstraction OpenRouter / Anthropic direct."""

from __future__ import annotations

from config.settings import get_settings

from .anthropic_direct import AnthropicDirectProvider
from .base import LLMProvider
from .openrouter import OpenRouterProvider


def get_llm_provider() -> LLMProvider:
    """Factory : retourne le provider selon LLM_PROVIDER."""
    settings = get_settings()
    if settings.llm_provider == "anthropic":
        return AnthropicDirectProvider()
    return OpenRouterProvider()


__all__ = ["LLMProvider", "get_llm_provider"]
