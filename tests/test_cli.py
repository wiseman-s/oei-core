"""Tests for the CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from oei.cli import app


def test_harmonise_cli(tmp_path: Path) -> None:
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
    exports = tmp_path / "exports"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "harmonise",
            str(data),
            str(mapping),
            "--export-dir",
            str(exports),
        ],
    )
    assert result.exit_code == 0
    assert (exports / "demo.csv").exists()
