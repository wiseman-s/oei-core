"""Tests for the I/O layer."""

from __future__ import annotations

from pathlib import Path

import pytest

from oei.errors import IOError
from oei.io.csv_reader import read_csv
from oei.io.hashing import hash_bytes
from oei.io.json_reader import read_json_records


def test_read_csv_missing(tmp_path: Path) -> None:
    with pytest.raises(IOError):
        read_csv(tmp_path / "missing.csv")


def test_read_json_records(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text('{"records": [{"a": 1}, {"a": 2}]}', encoding="utf-8")
    frame, digest = read_json_records(path)
    assert list(frame["a"]) == [1, 2]
    assert len(digest) == 64


def test_hash_bytes_deterministic() -> None:
    assert hash_bytes(b"oei") == hash_bytes(b"oei")
