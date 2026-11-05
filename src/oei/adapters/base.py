"""Base protocol for model adapters (PyPSA, OSeMOSYS, pandapower, ...)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from oei.models.dataset import Dataset


@runtime_checkable
class ModelAdapter(Protocol):
    """Protocol every OEI model adapter must implement."""

    name: str

    def to_model_inputs(self, dataset: Dataset) -> dict[str, object]:
        """Convert a harmonised OEI dataset into model-ready inputs."""
        ...

    def from_model_outputs(self, outputs: dict[str, object]) -> Dataset:
        """Convert model outputs back into an OEI dataset with provenance."""
        ...
