"""Scripted agent for tests: replays events and records the tasks it received."""
from __future__ import annotations

from typing import AsyncIterator

from core.agent.base import AgentEvent, AgentRuntime, AgentTask


class FakeAgentRuntime(AgentRuntime):
    def __init__(self, events: tuple[AgentEvent, ...] | None = None) -> None:
        self._events = events or (
            AgentEvent(kind="message", text="working"),
            AgentEvent(kind="done"),
        )
        self.tasks: list[AgentTask] = []

    async def run(self, task: AgentTask) -> AsyncIterator[AgentEvent]:
        self.tasks.append(task)
        for event in self._events:
            yield event
