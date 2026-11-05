"""Field-level schema definitions for the OEI data model."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class FieldType(str, Enum):
    """Supported semantic types in the OEI data model."""

    TIMESTAMP = "timestamp"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    CATEGORICAL = "categorical"
    GEO = "geo"


class FieldSpec(BaseModel):
    """Definition of a single field in a dataset schema."""

    name: str = Field(min_length=1)
    type: FieldType
    unit: str | None = None
    required: bool = True
    description: str | None = None
    allowed_values: list[str] | None = None
    minimum: float | None = None
    maximum: float | None = None
