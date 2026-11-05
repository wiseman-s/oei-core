"""Tests for the mapping engine."""

from __future__ import annotations

import pandas as pd
import pytest

from oei.errors import MappingError
from oei.mapping.engine import apply_mapping
from oei.mapping.mapping_config import MappingConfig


def test_apply_mapping(sample_frame: pd.DataFrame, sample_config: MappingConfig) -> None:
    ds = apply_mapping(sample_frame, sample_config, "deadbeef")
    assert len(ds.records) == 2
    assert ds.records[0].values["plant_name"] == "Olkaria I"
    assert ds.provenance.steps[0].operation == "map"


def test_missing_source_column(sample_mapping, sample_config) -> None:
    frame = pd.DataFrame({"date": ["2024-01-01"]})
    with pytest.raises(MappingError):
        apply_mapping(frame, sample_config, "deadbeef")


def test_load_bad_mapping(tmp_path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    with pytest.raises(MappingError):
        MappingConfig.from_yaml(bad)
