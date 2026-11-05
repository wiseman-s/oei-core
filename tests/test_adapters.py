"""Tests for model adapters."""

from __future__ import annotations

import pytest

from oei.adapters.osemosys import OSeMOSYSAdapter
from oei.adapters.registry import AdapterRegistry, default_registry
from oei.errors import AdapterError
from oei.models.dataset import Dataset, DatasetRecord
from oei.models.field import FieldSpec, FieldType
from oei.models.provenance import Provenance


def _build_dataset() -> Dataset:
    return Dataset(
        name="demo",
        schema_fields=[
            FieldSpec(name="timestamp", type=FieldType.TIMESTAMP),
            FieldSpec(name="plant_name", type=FieldType.STRING),
            FieldSpec(name="technology", type=FieldType.CATEGORICAL),
            FieldSpec(name="capacity_mw", type=FieldType.FLOAT, unit="MW"),
            FieldSpec(name="generation_mwh", type=FieldType.FLOAT, unit="MWh"),
        ],
        records=[
            DatasetRecord(
                values={
                    "timestamp": "2024-01-01T00:00:00Z",
                    "plant_name": "Olkaria I",
                    "technology": "Geothermal",
                    "capacity_mw": 45.0,
                    "generation_mwh": 320.5,
                }
            ),
            DatasetRecord(
                values={
                    "timestamp": "2024-06-01T00:00:00Z",
                    "plant_name": "Olkaria I",
                    "technology": "Geothermal",
                    "capacity_mw": 45.0,
                    "generation_mwh": 400.0,
                }
            ),
        ],
        provenance=Provenance(
            source_name="demo",
            source_uri="file://demo.csv",
            source_licence="CC-BY-4.0",
            source_hash="deadbeef",
        ),
    )


def test_to_model_inputs_aggregates_by_year() -> None:
    adapter = OSeMOSYSAdapter()
    outputs = adapter.to_model_inputs(_build_dataset())
    assert isinstance(outputs["capacity_by_year"], list)
    assert len(outputs["capacity_by_year"]) == 1
    assert outputs["capacity_by_year"][0]["CAPACITY_MW"] == 45.0
    assert outputs["generation_by_year"][0]["GENERATION_MWH"] == pytest.approx(720.5)


def test_to_model_inputs_rejects_bad_schema() -> None:
    adapter = OSeMOSYSAdapter()
    ds = Dataset(
        name="bad",
        schema_fields=[FieldSpec(name="timestamp", type=FieldType.TIMESTAMP)],
        records=[DatasetRecord(values={"timestamp": "2024-01-01"})],
        provenance=Provenance(
            source_name="bad",
            source_uri="file://bad",
            source_licence="CC-BY-4.0",
            source_hash="0" * 64,
        ),
    )
    with pytest.raises(AdapterError):
        adapter.to_model_inputs(ds)


def test_round_trip_preserves_values() -> None:
    adapter = OSeMOSYSAdapter()
    original = _build_dataset()
    outputs = adapter.to_model_inputs(original)
    restored = adapter.from_model_outputs(outputs)
    assert len(restored.records) == 1
    assert restored.records[0].values["capacity_mw"] == 45.0
    assert restored.records[0].values["generation_mwh"] == pytest.approx(720.5)
    assert restored.provenance.steps[0].operation == "adapter.from_model_outputs"


def test_registry_register_and_get() -> None:
    registry = AdapterRegistry(adapters=[])
    registry.register(OSeMOSYSAdapter())
    assert registry.names() == ["osemosys"]
    assert registry.get("osemosys").name == "osemosys"


def test_registry_unknown() -> None:
    registry = default_registry()
    with pytest.raises(AdapterError):
        registry.get("does-not-exist")
