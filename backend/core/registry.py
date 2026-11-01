"""Generic name -> factory registry. One instance per port (agent, sandbox, ...)."""
from __future__ import annotations

from typing import Callable, Generic, TypeVar

from core.config import Settings

T = TypeVar("T")


class ProviderNotFoundError(LookupError):
    """Config named a provider that was never registered."""


class Registry(Generic[T]):
    def __init__(self, kind: str) -> None:
        self._kind = kind
        self._factories: dict[str, Callable[[Settings], T]] = {}

    def register(self, name: str, factory: Callable[[Settings], T]) -> None:
        if name in self._factories:
            raise ValueError(f"{self._kind} provider '{name}' is already registered")
        self._factories[name] = factory

    def create(self, name: str, settings: Settings) -> T:
        factory = self._factories.get(name)
        if factory is None:
            available = ", ".join(self.names()) or "none"
            raise ProviderNotFoundError(
                f"Unknown {self._kind} provider '{name}'. Available: {available}"
            )
        return factory(settings)

    def names(self) -> list[str]:
        return sorted(self._factories)
