"""Mapping engine that applies a configuration to a raw DataFrame."""

from __future__ import annotations

from typing import Any

import pandas as pd

from oei.errors import MappingError
from oei.mapping.mapping_config import MappingConfig
from oei.mapping.transforms import resolve_transform
from oei.models.dataset import Dataset, DatasetRecord
from oei.models.provenance import Provenance


def _coerce(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def apply_mapping(
    frame: pd.DataFrame,
    config: MappingConfig,
    source_hash: str,
) -> Dataset:
    """Apply a mapping configuration to a DataFrame and produce a harmonised dataset."""
    missing = [m.source for m in config.mappings if m.source not in frame.columns]
    if missing:
        raise MappingError(f"Source columns missing from dataset: {missing}")

    resolved_transforms = {}
    for mapping in config.mappings:
        if mapping.transform is not None:
            resolved_transforms[mapping.target] = resolve_transform(mapping.transform)

    records: list[DatasetRecord] = []
    for raw in frame.to_dict(orient="records"):
        values: dict[str, Any] = {}
        for mapping in config.mappings:
            value = _coerce(raw.get(mapping.source))
            transform = resolved_transforms.get(mapping.target)
            if transform is not None and value is not None:
                value = transform.func(value)
            values[mapping.target] = value
        records.append(DatasetRecord(values=values))

    provenance = Provenance(
        source_name=config.source_name,
        source_uri=config.source_uri,
        source_licence=config.source_licence,
        source_hash=source_hash,
    )
    provenance.add_step(
        operation="map",
        description="Applied OEI mapping configuration to source columns.",
        mappings=[m.model_dump() for m in config.mappings],
    )

    return Dataset(
        name=config.source_name,
        schema_fields=list(config.schema_fields),
        records=records,
        provenance=provenance,
    )
