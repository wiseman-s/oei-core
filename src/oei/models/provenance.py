"""Provenance records describing where data came from and how it changed."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ProvenanceStep(BaseModel):
    """A single transformation step applied to a dataset."""

    operation: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Provenance(BaseModel):
    """Full provenance chain for a dataset."""

    source_name: str
    source_uri: str
    source_licence: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_hash: str
    schema_version: str = "0.1.0"
    steps: list[ProvenanceStep] = Field(default_factory=list)

    def add_step(self, operation: str, description: str, **parameters: Any) -> None:
        """Append a transformation step to the provenance chain."""
        self.steps.append(
            ProvenanceStep(
                operation=operation,
                description=description,
                parameters=parameters,
            )
        )
