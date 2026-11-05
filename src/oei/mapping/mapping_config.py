"""Declarative mapping configuration between source columns and OEI schema."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from oei.errors import MappingError
from oei.models.field import FieldSpec


class ColumnMapping(BaseModel):
    """Maps one source column to one OEI field."""

    source: str
    target: str
    transform: str | None = None
    unit_source: str | None = None
    unit_target: str | None = None


class MappingConfig(BaseModel):
    """A complete mapping configuration for one source dataset."""

    source_name: str
    source_licence: str
    source_uri: str
    schema_fields: list[FieldSpec] = Field(default_factory=list)
    mappings: list[ColumnMapping]
    timestamp_column: str | None = None
    default_unit: str | None = None

    @classmethod
    def from_yaml(cls, path: Path) -> MappingConfig:
        """Load a mapping configuration from a YAML file."""
        if not path.exists():
            raise MappingError(f"Mapping file not found: {path}")
        try:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise MappingError(f"Invalid YAML in {path}: {exc}") from exc
        if not isinstance(payload, dict):
            raise MappingError("Mapping file must contain a YAML mapping at the root.")
        try:
            return cls.model_validate(payload)
        except Exception as exc:
            raise MappingError(f"Invalid mapping configuration: {exc}") from exc
