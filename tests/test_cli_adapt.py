"""Tests for the ``oei adapt`` CLI command."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from oei.cli import app


def test_adapt_cli_osemosys(tmp_path: Path) -> None:
    data = Path("examples/data/kenya_generation_a.csv")
    mapping = Path("examples/mappings/source_a.yaml")
    exports = tmp_path / "exports"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "adapt",
            str(data),
            str(mapping),
            "--adapter",
            "osemosys",
            "--export-dir",
            str(exports),
        ],
    )
    assert result.exit_code == 0, result.output
    outputs = list(exports.glob("*_osemosys_*.csv"))
    assert len(outputs) == 3
