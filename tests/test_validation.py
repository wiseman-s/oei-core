"""Tests for the validation engine."""

from __future__ import annotations

import pandas as pd

from oei.mapping.engine import apply_mapping
from oei.mapping.mapping_config import MappingConfig
from oei.validation.quality_report import build_quality_report


def test_valid_dataset(sample_frame: pd.DataFrame, sample_config: MappingConfig) -> None:
    ds = apply_mapping(sample_frame, sample_config, "deadbeef")
    report = build_quality_report(ds)
    assert report.error_count == 0
    assert report.is_valid is True


def test_missing_required(tmp_path, sample_config: MappingConfig) -> None:
    frame = pd.DataFrame(
        {
            "date": ["2024-01-01", None],
            "plant": ["Olkaria I", "Olkaria II"],
            "capacity_mw": [45.0, 105.0],
        }
    )
    ds = apply_mapping(frame, sample_config, "deadbeef")
    report = build_quality_report(ds)
    assert report.error_count >= 1
    assert any(i.code == "required_missing" for i in report.issues)


def test_invalid_timestamp(sample_config: MappingConfig) -> None:
    frame = pd.DataFrame(
        {
            "date": ["not-a-date"],
            "plant": ["Olkaria I"],
            "capacity_mw": [45.0],
        }
    )
    ds = apply_mapping(frame, sample_config, "deadbeef")
    report = build_quality_report(ds)
    assert any(i.code == "invalid_timestamp" for i in report.issues)


def test_negative_generation_warns(sample_config: MappingConfig) -> None:
    frame = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "plant": ["Olkaria I"],
            "capacity_mw": [-10.0],
        }
    )
    ds = apply_mapping(frame, sample_config, "deadbeef")
    report = build_quality_report(ds)
    assert any(i.code == "below_minimum" for i in report.issues)
