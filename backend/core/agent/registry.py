from core.agent.base import AgentRuntime
from core.agent.fake import FakeAgentRuntime
from core.registry import Registry

AGENT_REGISTRY: Registry[AgentRuntime] = Registry("agent")
AGENT_REGISTRY.register("fake", lambda settings: FakeAgentRuntime())
# Real runtimes (e.g. claude_agent_sdk) register here; imported lazily to keep SDKs optional.
