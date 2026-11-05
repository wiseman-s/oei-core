"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from oei.mapping.mapping_config import MappingConfig


@pytest.fixture()
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "plant": ["Olkaria I", "Turkana Wind"],
            "technology": ["Geothermal", "Wind"],
            "capacity_mw": [45.0, 310.0],
            "generation_mwh": [320.5, 1240.0],
        }
    )


@pytest.fixture()
def sample_mapping(tmp_path: Path) -> Path:
    path = tmp_path / "mapping.yaml"
    path.write_text(
        """
source_name: demo
source_licence: CC-BY-4.0
source_uri: https://example.org/demo.csv
schema_fields:
  - name: timestamp
    type: timestamp
    required: true
  - name: plant_name
    type: string
    required: true
  - name: capacity_mw
    type: float
    required: true
    minimum: 0
mappings:
  - source: date
    target: timestamp
  - source: plant
    target: plant_name
  - source: capacity_mw
    target: capacity_mw
""",
        encoding="utf-8",
    )
    return path


@pytest.fixture()
def sample_config(sample_mapping: Path) -> MappingConfig:
    return MappingConfig.from_yaml(sample_mapping)
