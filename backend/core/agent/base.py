"""Port: an agent framework that can read/write files in a workspace to complete a task."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncIterator, Literal

from pydantic import BaseModel, ConfigDict, Field

AgentEventKind = Literal["message", "tool_use", "error", "done"]


class AgentTask(BaseModel):
    model_config = ConfigDict(frozen=True)

    prompt: str
    cwd: Path
    allowed_tools: tuple[str, ...] = ("Read", "Write", "Edit", "Glob", "Grep")
    max_turns: int = Field(default=30, ge=1)


class AgentEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: AgentEventKind
    text: str = ""


class AgentRuntime(ABC):
    """Extend this to add a new agent framework, then register it in registry.py."""

    @abstractmethod
    def run(self, task: AgentTask) -> AsyncIterator[AgentEvent]:
        """Execute the task confined to task.cwd, streaming events; last event is 'done' or 'error'."""
