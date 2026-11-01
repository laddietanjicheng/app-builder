"""Port: a text-completion LLM. Extend LLMClient to add a provider, then register it."""
from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

_FENCE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)


class LLMOutputError(ValueError):
    """The model replied, but not with usable structured output."""


def parse_json_output(raw: str, schema: type[T]) -> T:
    text = raw.strip()
    fenced = _FENCE.match(text)
    if fenced:
        text = fenced.group(1)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMOutputError(f"Model output was not valid JSON: {exc}") from exc
    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise LLMOutputError(
            f"Model output did not match the expected schema: {exc}"
        ) from exc


class LLMClient(ABC):
    @abstractmethod
    async def complete(self, prompt: str, *, system: str | None = None) -> str:
        """Return the model's text reply."""

    async def complete_json(
        self, prompt: str, schema: type[T], *, system: str | None = None
    ) -> T:
        """Ask for JSON matching `schema`. Providers with native structured output may override."""
        schema_json = json.dumps(schema.model_json_schema())
        full_prompt = (
            f"{prompt}\n\nRespond with ONLY a JSON object matching this JSON schema, "
            f"with no other text:\n{schema_json}"
        )
        raw = await self.complete(full_prompt, system=system)
        return parse_json_output(raw, schema)
