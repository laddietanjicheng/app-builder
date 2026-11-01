from core.config import Settings
from core.llm.anthropic_client import AnthropicLLMClient
from core.llm.base import LLMClient
from core.llm.fake import FakeLLMClient
from core.registry import Registry

LLM_REGISTRY: Registry[LLMClient] = Registry("llm")


def _build_anthropic(settings: Settings) -> LLMClient:
    api_key = settings.require_secret("anthropic_api_key")
    from anthropic import AsyncAnthropic  # lazy: SDK only needed when selected

    return AnthropicLLMClient(AsyncAnthropic(api_key=api_key), model=settings.llm_model)


LLM_REGISTRY.register("fake", lambda settings: FakeLLMClient())
LLM_REGISTRY.register("anthropic", _build_anthropic)
