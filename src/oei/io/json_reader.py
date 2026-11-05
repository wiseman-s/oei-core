"""JSON dataset reader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from oei.errors import IOError
from oei.io.hashing import hash_file


def read_json_records(path: Path) -> tuple[pd.DataFrame, str]:
    """Read a JSON file containing a list of records into a DataFrame."""
    if not path.exists():
        raise IOError(f"JSON file not found: {path}")
    try:
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise IOError(f"Failed to parse JSON {path}: {exc}") from exc
    if isinstance(payload, dict) and "records" in payload:
        payload = payload["records"]
    if not isinstance(payload, list):
        raise IOError("JSON dataset must be a list of records or an object with a 'records' key.")
    return pd.DataFrame(payload), hash_file(path)
