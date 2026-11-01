"""Anthropic Messages API adapter. The SDK client is injected so tests need no network."""
from __future__ import annotations

from typing import Any

from core.llm.base import LLMClient


class AnthropicLLMClient(LLMClient):
    def __init__(self, sdk_client: Any, model: str, max_tokens: int = 4096) -> None:
        self._client = sdk_client
        self._model = model
        self._max_tokens = max_tokens

    async def complete(self, prompt: str, *, system: str | None = None) -> str:
        kwargs: dict[str, Any] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        response = await self._client.messages.create(**kwargs)
        return "".join(
            block.text for block in response.content if block.type == "text"
        )
