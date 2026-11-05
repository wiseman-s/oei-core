"""CSV dataset writer."""

from __future__ import annotations

from pathlib import Path

from oei.models.dataset import Dataset


def write_csv(dataset: Dataset, path: Path) -> Path:
    """Write a dataset to CSV, returning the written path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = dataset_to_frame(dataset)
    frame.to_csv(path, index=False)
    return path


def dataset_to_frame(dataset: Dataset):  # type: ignore[no-untyped-def]
    import pandas as pd

    return pd.DataFrame(dataset.to_rows(), columns=dataset.field_names())
