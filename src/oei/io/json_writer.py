"""JSON dataset writer with embedded provenance."""

from __future__ import annotations

import json
from pathlib import Path

from oei.models.dataset import Dataset


def write_json(dataset: Dataset, path: Path) -> Path:
    """Write a dataset to JSON, including provenance metadata."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "name": dataset.name,
        "schema": [f.model_dump() for f in dataset.schema_fields],
        "provenance": dataset.provenance.model_dump(mode="json"),
        "records": dataset.to_rows(),
    }
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path
