"""Adapter registry so OEI can discover and route to model adapters by name."""

from __future__ import annotations

from collections.abc import Iterable

from oei.adapters.base import ModelAdapter
from oei.adapters.osemosys import OSeMOSYSAdapter
from oei.errors import AdapterError


def _built_in_adapters() -> Iterable[ModelAdapter]:
    yield OSeMOSYSAdapter()


class AdapterRegistry:
    """Discoverable collection of model adapters."""

    def __init__(self, adapters: Iterable[ModelAdapter] | None = None) -> None:
        self._adapters: dict[str, ModelAdapter] = {}
        for adapter in adapters if adapters is not None else _built_in_adapters():
            self.register(adapter)

    def register(self, adapter: ModelAdapter) -> None:
        if adapter.name in self._adapters:
            raise AdapterError(f"Adapter already registered: {adapter.name}")
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> ModelAdapter:
        try:
            return self._adapters[name]
        except KeyError as exc:
            raise AdapterError(f"Unknown adapter: {name}") from exc

    def names(self) -> list[str]:
        return sorted(self._adapters)


def default_registry() -> AdapterRegistry:
    """Return a registry pre-populated with OEI's built-in adapters."""
    return AdapterRegistry()
