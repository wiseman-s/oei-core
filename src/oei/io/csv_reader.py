"""CSV dataset reader."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from oei.errors import IOError
from oei.io.hashing import hash_file


def read_csv(path: Path) -> tuple[pd.DataFrame, str]:
    """Read a CSV file into a DataFrame.

    Args:
        path: Path to the CSV file.

    Returns:
        A tuple of the loaded DataFrame and its SHA-256 digest.

    Raises:
        IOError: If the file cannot be read.
    """
    if not path.exists():
        raise IOError(f"CSV file not found: {path}")
    try:
        frame = pd.read_csv(path)
    except Exception as exc:
        raise IOError(f"Failed to read CSV {path}: {exc}") from exc
    return frame, hash_file(path)
