"""Command-line interface for OEI Core."""

from __future__ import annotations

from pathlib import Path

import typer
from pandas import DataFrame
from rich.console import Console
from rich.table import Table

from oei.adapters.registry import default_registry
from oei.config import load_settings
from oei.io.csv_reader import read_csv
from oei.io.csv_writer import write_csv
from oei.io.json_reader import read_json_records
from oei.io.json_writer import write_json
from oei.logging import configure_logging
from oei.mapping.engine import apply_mapping
from oei.mapping.mapping_config import MappingConfig
from oei.provenance.store import SqliteStore
from oei.validation.quality_report import build_quality_report

app = typer.Typer(help="OEI Core: open energy data integration and validation engine.")
console = Console()


@app.command()
def harmonise(
    source: Path = typer.Argument(..., help="Source dataset path."),
    mapping: Path = typer.Argument(..., help="Mapping configuration YAML path."),
    source_format: str = typer.Option("csv", "--format", "-f", help="csv or json."),
    export_dir: Path = typer.Option(Path("./exports"), "--export-dir", "-e"),
    as_json: bool = typer.Option(False, "--json", help="Export as JSON instead of CSV."),
    record: bool = typer.Option(
        False,
        "--record",
        help="Record provenance in the local SQLite store.",
    ),
    database: Path = typer.Option(
        Path.home() / ".oei" / "provenance.db",
        "--database",
        "-d",
        help="SQLite database path for provenance records.",
    ),
) -> None:
    """Harmonise a dataset, validate it and export the result."""
    settings = load_settings()
    configure_logging(settings.log_level)

    if source_format == "csv":
        frame, digest = read_csv(source)
    elif source_format == "json":
        frame, digest = read_json_records(source)
    else:
        raise typer.BadParameter(f"Unsupported source format: {source_format}")

    config = MappingConfig.from_yaml(mapping)
    dataset = apply_mapping(frame, config, digest)
    report = build_quality_report(dataset)

    table = Table(title=f"Quality report: {dataset.name}")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Rows", str(report.total_rows))
    table.add_row("Errors", str(report.error_count))
    table.add_row("Warnings", str(report.warning_count))
    table.add_row("Info", str(report.info_count))
    table.add_row("Valid", "yes" if report.is_valid else "no")
    console.print(table)

    export_dir.mkdir(parents=True, exist_ok=True)

    if as_json:
        out = write_json(dataset, export_dir / f"{dataset.name}.json")
    else:
        out = write_csv(dataset, export_dir / f"{dataset.name}.csv")

    console.print(f"[green]Exported:[/green] {out}")

    if record:
        store = SqliteStore(database)
        try:
            record_id = store.record(dataset, report)
        finally:
            store.close()

        console.print(f"[green]Recorded:[/green] provenance id {record_id} in {database}")


@app.command()
def adapt(
    source: Path = typer.Argument(..., help="Source dataset path."),
    mapping: Path = typer.Argument(..., help="Mapping configuration YAML path."),
    adapter_name: str = typer.Option("osemosys", "--adapter", "-a"),
    source_format: str = typer.Option("csv", "--format", "-f"),
    export_dir: Path = typer.Option(Path("./exports"), "--export-dir", "-e"),
) -> None:
    """Convert a harmonised dataset into a model adapter's parameter tables."""
    settings = load_settings()
    configure_logging(settings.log_level)

    if source_format == "csv":
        frame, digest = read_csv(source)
    elif source_format == "json":
        frame, digest = read_json_records(source)
    else:
        raise typer.BadParameter(f"Unsupported source format: {source_format}")

    config = MappingConfig.from_yaml(mapping)
    dataset = apply_mapping(frame, config, digest)

    adapter = default_registry().get(adapter_name)
    tables = adapter.to_model_inputs(dataset)

    export_dir.mkdir(parents=True, exist_ok=True)

    for table_name, rows in tables.items():
        if not isinstance(rows, list) or not rows:
            continue

        out_path = export_dir / f"{dataset.name}_{adapter_name}_{table_name}.csv"
        DataFrame(rows).to_csv(out_path, index=False)
        console.print(f"[green]Wrote[/green] {out_path}")


@app.command("provenance-list")
def provenance_list(
    database: Path = typer.Option(
        Path.home() / ".oei" / "provenance.db",
        "--database",
        "-d",
        help="SQLite database path.",
    ),
) -> None:
    """List recorded provenance entries from the local SQLite store."""
    if not database.exists():
        console.print(f"[yellow]No provenance database at[/yellow] {database}")
        raise typer.Exit(code=0)

    store = SqliteStore(database)

    try:
        rows = store._conn.execute(
            """
            SELECT id, dataset_name, source_hash, is_valid, error_count, recorded_at
            FROM provenance
            ORDER BY id DESC
            LIMIT 50
            """
        ).fetchall()
    finally:
        store.close()

    table = Table(title=f"Provenance records ({database})")
    table.add_column("ID", justify="right")
    table.add_column("Dataset")
    table.add_column("Source hash", overflow="fold")
    table.add_column("Valid")
    table.add_column("Errors", justify="right")
    table.add_column("Recorded at")

    for row in rows:
        table.add_row(
            str(row[0]),
            str(row[1]),
            str(row[2])[:16] + "…",
            "yes" if row[3] else "no",
            str(row[4]),
            str(row[5]),
        )

    console.print(table)


@app.command("provenance-show")
def provenance_show(
    record_id: int = typer.Argument(..., help="Provenance record id."),
    database: Path = typer.Option(
        Path.home() / ".oei" / "provenance.db",
        "--database",
        "-d",
        help="SQLite database path.",
    ),
) -> None:
    """Show a single provenance record as JSON."""
    if not database.exists():
        raise typer.BadParameter(f"Database not found: {database}")

    store = SqliteStore(database)

    try:
        payload = store.get(record_id)
    finally:
        store.close()

    if payload is None:
        console.print(f"[red]No record with id {record_id}[/red]")
        raise typer.Exit(code=1)

    console.print_json(data=payload)
