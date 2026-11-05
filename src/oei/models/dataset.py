"""The canonical OEI dataset model."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from oei.models.field import FieldSpec
from oei.models.provenance import Provenance


class DatasetRecord(BaseModel):
    """A single harmonised record in the OEI data model."""

    values: dict[str, Any]


class Dataset(BaseModel):
    """A harmonised dataset with schema, records and provenance."""

    name: str
    schema_fields: list[FieldSpec] = Field(default_factory=list)
    records: list[DatasetRecord] = Field(default_factory=list)
    provenance: Provenance

    def field_names(self) -> list[str]:
        return [f.name for f in self.schema_fields]

    def to_rows(self) -> list[dict[str, Any]]:
        return [record.values for record in self.records]
