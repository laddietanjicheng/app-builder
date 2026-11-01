"""Central settings. Provider names here are resolved by core.factory."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKEND_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    # Provider selection (the "which framework/service" switches)
    agent: str = Field(default="claude_agent_sdk", alias="AGENT")
    llm: str = Field(default="anthropic", alias="LLM")
    prompt_store: str = Field(default="file", alias="PROMPT_STORE")
    tracer: str = Field(default="console", alias="TRACER")
    object_store: str = Field(default="local_fs", alias="OBJECT_STORE")
    sandbox: str = Field(default="local_process", alias="SANDBOX")

    # Paths
    data_dir: Path = Field(default=_REPO_ROOT / "data", alias="DATA_DIR")
    prompts_dir: Path = Field(default=_BACKEND_ROOT / "prompts", alias="PROMPTS_DIR")
    app_template_dir: Path = Field(
        default=_BACKEND_ROOT / "app_template", alias="APP_TEMPLATE_DIR"
    )

    # Secrets (optional at import time; providers validate when used)
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    # Limits
    max_upload_bytes: int = Field(default=10 * 1024 * 1024, alias="MAX_UPLOAD_BYTES")
    max_build_retries: int = Field(default=3, alias="MAX_BUILD_RETRIES")

    def require_secret(self, name: str) -> str:
        value = getattr(self, name)
        if not value:
            raise RuntimeError(f"Missing required setting: {name.upper()}")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
