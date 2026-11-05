"""Persistent provenance store.

Provenance records are the audit trail of every harmonisation: which source,
which mapping, which OEI version, when, and with what quality outcome. This
module exposes a tiny protocol and a SQLite implementation suitable for
local-first use. Deployments that need multi-writer concurrency can implement
``ProvenanceStore`` against Postgres without touching call sites.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Protocol

from oei.models.dataset import Dataset
from oei.models.quality import QualityReport

_SCHEMA = """
CREATE TABLE IF NOT EXISTS provenance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name    TEXT NOT NULL,
    source_name     TEXT NOT NULL,
    source_uri      TEXT NOT NULL,
    source_licence  TEXT NOT NULL,
    source_hash     TEXT NOT NULL,
    schema_version  TEXT NOT NULL,
    retrieved_at    TEXT NOT NULL,
    recorded_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    error_count     INTEGER NOT NULL DEFAULT 0,
    warning_count   INTEGER NOT NULL DEFAULT 0,
    is_valid        INTEGER NOT NULL DEFAULT 1,
    payload_json    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_provenance_source_hash
    ON provenance (source_hash);

CREATE INDEX IF NOT EXISTS idx_provenance_dataset_name
    ON provenance (dataset_name);

CREATE INDEX IF NOT EXISTS idx_provenance_recorded_at
    ON provenance (recorded_at DESC);
"""


class ProvenanceStore(Protocol):
    """Protocol for provenance persistence backends."""

    def record(self, dataset: Dataset, report: QualityReport | None = None) -> int:
        """Persist a dataset's provenance and return the record id."""
        ...

    def get(self, record_id: int) -> dict[str, object] | None:
        """Return the stored payload for a record id, or ``None``."""
        ...

    def count(self) -> int:
        """Return the number of stored provenance records."""
        ...

    def close(self) -> None:
        """Release any held resources."""
        ...


class SqliteStore:
    """SQLite-backed provenance store.

    Args:
        path: Path to the SQLite database file. The parent directory is
            created if missing. Pass ``":memory:"`` for an in-memory store.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        if isinstance(path, Path):
            path.parent.mkdir(parents=True, exist_ok=True)
            self._path = str(path)
        else:
            self._path = path
        self._conn = sqlite3.connect(self._path)
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def record(self, dataset: Dataset, report: QualityReport | None = None) -> int:
        """Persist provenance and (optionally) quality counts for a dataset."""
        provenance = dataset.provenance
        payload = {
            "dataset": {
                "name": dataset.name,
                "schema_fields": [f.model_dump() for f in dataset.schema_fields],
                "record_count": len(dataset.records),
            },
            "provenance": provenance.model_dump(mode="json"),
            "quality": report.model_dump(mode="json") if report is not None else None,
        }
        cursor = self._conn.execute(
            """
            INSERT INTO provenance (
                dataset_name, source_name, source_uri, source_licence,
                source_hash, schema_version, retrieved_at,
                error_count, warning_count, is_valid, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dataset.name,
                provenance.source_name,
                provenance.source_uri,
                provenance.source_licence,
                provenance.source_hash,
                provenance.schema_version,
                provenance.retrieved_at.isoformat(),
                report.error_count if report is not None else 0,
                report.warning_count if report is not None else 0,
                1 if (report is None or report.is_valid) else 0,
                json.dumps(payload, default=str),
            ),
        )
        self._conn.commit()
        return int(cursor.lastrowid or 0)

    def get(self, record_id: int) -> dict[str, object] | None:
        row = self._conn.execute(
            "SELECT payload_json FROM provenance WHERE id = ?", (record_id,)
        ).fetchone()
        if row is None:
            return None
        parsed: dict[str, object] = json.loads(row[0])
        return parsed

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) FROM provenance").fetchone()
        return int(row[0])

    def find_by_hash(self, source_hash: str) -> list[dict[str, object]]:
        rows = self._conn.execute(
            "SELECT payload_json FROM provenance WHERE source_hash = ? ORDER BY id DESC",
            (source_hash,),
        ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def close(self) -> None:
        self._conn.close()
