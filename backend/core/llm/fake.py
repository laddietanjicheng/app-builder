"""Scripted LLM for tests: returns canned replies in order and records every call."""
from __future__ import annotations

from dataclasses import dataclass

from core.llm.base import LLMClient


@dataclass(frozen=True)
class LLMCall:
    prompt: str
    system: str | None


class FakeLLMClient(LLMClient):
    def __init__(self, responses: list[str] | None = None) -> None:
        self._responses = list(responses or [])
        self.calls: list[LLMCall] = []

    async def complete(self, prompt: str, *, system: str | None = None) -> str:
        self.calls.append(LLMCall(prompt=prompt, system=system))
        assert self._responses, "FakeLLMClient has no scripted response left"
        return self._responses.pop(0)
