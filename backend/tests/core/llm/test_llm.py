from types import SimpleNamespace

import pytest
from pydantic import BaseModel

from core.config import Settings
from core.llm.anthropic_client import AnthropicLLMClient
from core.llm.base import LLMOutputError
from core.llm.fake import FakeLLMClient
from core.llm.registry import LLM_REGISTRY


class Question(BaseModel):
    text: str
    options: list[str]


# ---- base behaviour (exercised through the fake) ----

async def test_complete_returns_scripted_text_and_records_call():
    llm = FakeLLMClient(["hello"])

    result = await llm.complete("hi", system="be nice")

    assert result == "hello"
    assert llm.calls[0].prompt == "hi"
    assert llm.calls[0].system == "be nice"


async def test_complete_json_parses_into_schema():
    llm = FakeLLMClient(['{"text": "Who uses it?", "options": ["me", "team"]}'])

    result = await llm.complete_json("ask", Question)

    assert result == Question(text="Who uses it?", options=["me", "team"])


async def test_complete_json_strips_markdown_fences():
    llm = FakeLLMClient(['```json\n{"text": "t", "options": []}\n```'])

    result = await llm.complete_json("ask", Question)

    assert result.text == "t"


async def test_complete_json_prompt_includes_schema():
    llm = FakeLLMClient(['{"text": "t", "options": []}'])

    await llm.complete_json("ask", Question)

    sent = llm.calls[0].prompt
    assert "ask" in sent and "options" in sent and "JSON" in sent


async def test_complete_json_raises_on_invalid_json():
    llm = FakeLLMClient(["not json at all"])

    with pytest.raises(LLMOutputError, match="valid JSON"):
        await llm.complete_json("ask", Question)


async def test_complete_json_raises_on_schema_mismatch():
    llm = FakeLLMClient(['{"text": "t"}'])

    with pytest.raises(LLMOutputError, match="schema"):
        await llm.complete_json("ask", Question)


async def test_fake_raises_when_script_exhausted():
    llm = FakeLLMClient([])

    with pytest.raises(AssertionError, match="no scripted response"):
        await llm.complete("hi")


# ---- anthropic adapter (stubbed SDK client, no network) ----

class StubMessages:
    def __init__(self) -> None:
        self.kwargs: dict = {}

    async def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text="part one "),
                     SimpleNamespace(type="text", text="part two")]
        )


async def test_anthropic_complete_joins_text_blocks_and_passes_params():
    messages = StubMessages()
    client = AnthropicLLMClient(
        sdk_client=SimpleNamespace(messages=messages), model="m-1", max_tokens=123
    )

    result = await client.complete("question", system="sys")

    assert result == "part one part two"
    assert messages.kwargs["model"] == "m-1"
    assert messages.kwargs["max_tokens"] == 123
    assert messages.kwargs["system"] == "sys"
    assert messages.kwargs["messages"] == [{"role": "user", "content": "question"}]


async def test_anthropic_omits_system_when_not_given():
    messages = StubMessages()
    client = AnthropicLLMClient(sdk_client=SimpleNamespace(messages=messages), model="m")

    await client.complete("q")

    assert "system" not in messages.kwargs


# ---- registry ----

def test_registry_lists_fake_and_anthropic():
    assert {"fake", "anthropic"} <= set(LLM_REGISTRY.names())


def test_registry_creates_fake():
    assert isinstance(LLM_REGISTRY.create("fake", Settings()), FakeLLMClient)


def test_anthropic_without_api_key_fails_fast():
    settings = Settings(ANTHROPIC_API_KEY=None, _env_file=None)

    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        LLM_REGISTRY.create("anthropic", settings)


def test_anthropic_with_api_key_builds_client_using_configured_model():
    settings = Settings(
        ANTHROPIC_API_KEY="test-key", LLM_MODEL="model-x", _env_file=None
    )

    client = LLM_REGISTRY.create("anthropic", settings)

    assert isinstance(client, AnthropicLLMClient)
    assert client._model == "model-x"
