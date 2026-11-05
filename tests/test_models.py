"""Tests for OEI data models."""

from __future__ import annotations

from oei.models.dataset import Dataset, DatasetRecord
from oei.models.field import FieldSpec, FieldType
from oei.models.provenance import Provenance
from oei.models.quality import QualityIssue, QualityReport, Severity


def test_dataset_field_names() -> None:
    ds = Dataset(
        name="demo",
        schema_fields=[FieldSpec(name="timestamp", type=FieldType.TIMESTAMP)],
        records=[DatasetRecord(values={"timestamp": "2024-01-01"})],
        provenance=Provenance(
            source_name="demo",
            source_uri="file://demo.csv",
            source_licence="CC-BY-4.0",
            source_hash="deadbeef",
        ),
    )
    assert ds.field_names() == ["timestamp"]
    assert ds.to_rows() == [{"timestamp": "2024-01-01"}]


def test_quality_report_counts() -> None:
    report = QualityReport(
        dataset_name="demo",
        total_rows=2,
        issues=[
            QualityIssue(code="x", message="m", severity=Severity.ERROR),
            QualityIssue(code="y", message="m", severity=Severity.WARNING),
            QualityIssue(code="z", message="m", severity=Severity.INFO),
        ],
    )
    assert report.error_count == 1
    assert report.warning_count == 1
    assert report.info_count == 1
    assert report.is_valid is False


def test_provenance_step_appended() -> None:
    p = Provenance(
        source_name="demo",
        source_uri="file://demo.csv",
        source_licence="CC-BY-4.0",
        source_hash="deadbeef",
    )
    p.add_step("map", "Applied mapping", count=3)
    assert len(p.steps) == 1
    assert p.steps[0].parameters["count"] == 3
