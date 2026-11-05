"""Tests for the SQLite provenance store."""

from __future__ import annotations

from pathlib import Path

from oei.models.dataset import Dataset, DatasetRecord
from oei.models.field import FieldSpec, FieldType
from oei.models.provenance import Provenance
from oei.models.quality import QualityIssue, QualityReport, Severity
from oei.provenance.store import SqliteStore


def _build_dataset() -> Dataset:
    return Dataset(
        name="demo",
        schema_fields=[FieldSpec(name="timestamp", type=FieldType.TIMESTAMP)],
        records=[DatasetRecord(values={"timestamp": "2024-01-01T00:00:00Z"})],
        provenance=Provenance(
            source_name="demo",
            source_uri="file://demo.csv",
            source_licence="CC-BY-4.0",
            source_hash="a" * 64,
        ),
    )


def _build_report(valid: bool) -> QualityReport:
    report = QualityReport(dataset_name="demo", total_rows=1)
    if not valid:
        report.issues.append(QualityIssue(code="x", message="m", severity=Severity.ERROR))
    return report


def test_record_and_get_in_memory() -> None:
    store = SqliteStore()
    try:
        record_id = store.record(_build_dataset(), _build_report(valid=True))
        assert record_id >= 1
        payload = store.get(record_id)
        assert payload is not None
        assert payload["dataset"]["name"] == "demo"  # type: ignore[index]
        assert payload["provenance"]["source_hash"] == "a" * 64  # type: ignore[index]
    finally:
        store.close()


def test_invalid_report_marks_not_valid(tmp_path: Path) -> None:
    db = tmp_path / "prov.db"
    store = SqliteStore(db)
    try:
        record_id = store.record(_build_dataset(), _build_report(valid=False))
        row = store._conn.execute(
            "SELECT is_valid, error_count FROM provenance WHERE id = ?",
            (record_id,),
        ).fetchone()
        assert row == (0, 1)
    finally:
        store.close()


def test_find_by_hash(tmp_path: Path) -> None:
    db = tmp_path / "prov.db"
    store = SqliteStore(db)
    try:
        store.record(_build_dataset())
        store.record(_build_dataset())
        matches = store.find_by_hash("a" * 64)
        assert len(matches) == 2
    finally:
        store.close()


def test_get_missing_returns_none() -> None:
    store = SqliteStore()
    try:
        assert store.get(999_999) is None
        assert store.count() == 0
    finally:
        store.close()


def test_record_survives_reopen(tmp_path: Path) -> None:
    db = tmp_path / "prov.db"
    store = SqliteStore(db)
    record_id = store.record(_build_dataset(), _build_report(valid=True))
    store.close()

    store2 = SqliteStore(db)
    try:
        assert store2.count() == 1
        assert store2.get(record_id) is not None
    finally:
        store2.close()


def test_cli_record_and_list(tmp_path: Path) -> None:
    from typer.testing import CliRunner

    from oei.cli import app

    data = tmp_path / "data.csv"
    data.write_text("date,plant,capacity_mw\n2024-01-01,Olkaria I,45.0\n", encoding="utf-8")
    mapping = tmp_path / "mapping.yaml"
    mapping.write_text(
        """
source_name: demo
source_licence: CC-BY-4.0
source_uri: https://example.org/demo.csv
schema_fields:
  - name: timestamp
    type: timestamp
  - name: plant_name
    type: string
  - name: capacity_mw
    type: float
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
    db = tmp_path / "prov.db"
    exports = tmp_path / "exports"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "harmonise",
            str(data),
            str(mapping),
            "--record",
            "--database",
            str(db),
            "--export-dir",
            str(exports),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "provenance id" in result.output

    store = SqliteStore(db)
    try:
        assert store.count() == 1
    finally:
        store.close()

    list_result = runner.invoke(app, ["provenance-list", "--database", str(db)])
    assert list_result.exit_code == 0, list_result.output
    assert "demo" in list_result.output


def test_cli_provenance_show(tmp_path: Path) -> None:
    from typer.testing import CliRunner

    from oei.cli import app

    db = tmp_path / "prov.db"
    store = SqliteStore(db)
    record_id = store.record(_build_dataset())
    store.close()

    runner = CliRunner()
    result = runner.invoke(app, ["provenance-show", str(record_id), "--database", str(db)])
    assert result.exit_code == 0, result.output
    assert "demo" in result.output


def test_cli_provenance_show_missing(tmp_path: Path) -> None:
    from typer.testing import CliRunner

    from oei.cli import app

    db = tmp_path / "prov.db"
    SqliteStore(db).close()
    runner = CliRunner()
    result = runner.invoke(app, ["provenance-show", "9999", "--database", str(db)])
    assert result.exit_code == 1
