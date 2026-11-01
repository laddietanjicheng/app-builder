import pytest

from core.config import Settings
from core.registry import ProviderNotFoundError, Registry


def make_settings() -> Settings:
    return Settings()


def test_create_returns_instance_built_by_registered_factory():
    registry: Registry[str] = Registry("thing")
    registry.register("a", lambda settings: "built-a")

    assert registry.create("a", make_settings()) == "built-a"


def test_factory_receives_settings():
    registry: Registry[object] = Registry("thing")
    settings = make_settings()
    registry.register("a", lambda s: s)

    assert registry.create("a", settings) is settings


def test_unknown_name_raises_error_listing_available_providers():
    registry: Registry[str] = Registry("agent")
    registry.register("fake", lambda s: "x")
    registry.register("real", lambda s: "y")

    with pytest.raises(ProviderNotFoundError) as exc:
        registry.create("nope", make_settings())

    message = str(exc.value)
    assert "agent" in message and "nope" in message
    assert "fake" in message and "real" in message


def test_duplicate_registration_is_rejected():
    registry: Registry[str] = Registry("thing")
    registry.register("a", lambda s: "1")

    with pytest.raises(ValueError, match="already registered"):
        registry.register("a", lambda s: "2")


def test_names_are_sorted():
    registry: Registry[str] = Registry("thing")
    registry.register("b", lambda s: "")
    registry.register("a", lambda s: "")

    assert registry.names() == ["a", "b"]


def test_registries_are_independent_per_port():
    first: Registry[str] = Registry("sandbox")
    second: Registry[str] = Registry("object_store")
    first.register("local", lambda s: "sandbox")
    second.register("local", lambda s: "store")

    assert first.create("local", make_settings()) == "sandbox"
    assert second.create("local", make_settings()) == "store"
