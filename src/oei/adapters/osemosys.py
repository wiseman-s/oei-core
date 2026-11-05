"""OSeMOSYS adapter: convert harmonised OEI datasets into OSeMOSYS-ready tables.

OSeMOSYS is a long-term energy-system and capacity planning model. It consumes
structured CSV parameter tables keyed by technology, year, and (for time-sliced
parameters) timeslice. This adapter produces a minimal, reproducible set of
those tables from an OEI dataset that conforms to the OEI generation schema,
so OEI can be the front door to OSeMOSYS workflows without duplicating the
model itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from oei.adapters.base import ModelAdapter
from oei.errors import AdapterError
from oei.models.dataset import Dataset, DatasetRecord
from oei.models.field import FieldSpec, FieldType
from oei.models.provenance import Provenance

_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "timestamp",
    "plant_name",
    "technology",
    "capacity_mw",
    "generation_mwh",
)


@dataclass(frozen=True)
class OSeMOSYSExport:
    """Bundle of OSeMOSYS parameter tables produced by the adapter."""

    technologies: list[dict[str, object]]
    capacity_by_year: list[dict[str, object]]
    generation_by_year: list[dict[str, object]]


def _extract_year(timestamp: object) -> int:
    text = str(timestamp)
    try:
        return int(text[:4])
    except (TypeError, ValueError) as exc:
        raise AdapterError(f"Cannot extract year from timestamp: {timestamp!r}") from exc


class OSeMOSYSAdapter(ModelAdapter):
    """Convert an OEI generation dataset into OSeMOSYS parameter tables."""

    name: str = "osemosys"

    def __init__(self, base_year: int = 2024) -> None:
        self.base_year = base_year

    def _assert_schema(self, dataset: Dataset) -> None:
        present = set(dataset.field_names())
        missing = [field for field in _REQUIRED_FIELDS if field not in present]
        if missing:
            raise AdapterError(f"Dataset is missing required fields: {missing}")

    def _index(self, dataset: Dataset) -> dict[tuple[str, str, int], dict[str, float]]:
        self._assert_schema(dataset)
        index: dict[tuple[str, str, int], dict[str, float]] = {}
        for record in dataset.records:
            year = _extract_year(record.values.get("timestamp"))
            key = (
                str(record.values["plant_name"]),
                str(record.values["technology"]),
                year,
            )
            bucket = index.setdefault(key, {"capacity_mw": 0.0, "generation_mwh": 0.0})
            bucket["capacity_mw"] = max(bucket["capacity_mw"], float(record.values["capacity_mw"]))
            bucket["generation_mwh"] += float(record.values["generation_mwh"])
        return index

    def to_model_inputs(self, dataset: Dataset) -> dict[str, object]:
        """Produce OSeMOSYS parameter tables from an OEI dataset.

        Args:
            dataset: A harmonised OEI generation dataset.

        Returns:
            A dict with keys ``technologies``, ``capacity_by_year`` and
            ``generation_by_year``; each value is a list of row dicts
            suitable for writing to CSV.

        Raises:
            AdapterError: If the dataset schema is incompatible.
        """
        index = self._index(dataset)
        technologies: list[dict[str, object]] = []
        capacity_rows: list[dict[str, object]] = []
        generation_rows: list[dict[str, object]] = []

        for (plant, tech, year), metrics in sorted(index.items()):
            technologies.append(
                {
                    "TECHNOLOGY": tech,
                    "PLANT": plant,
                    "FIRST_YEAR": self.base_year,
                    "LAST_YEAR": max(year, self.base_year),
                }
            )
            capacity_rows.append(
                {
                    "TECHNOLOGY": tech,
                    "PLANT": plant,
                    "YEAR": year,
                    "CAPACITY_MW": round(metrics["capacity_mw"], 6),
                }
            )
            generation_rows.append(
                {
                    "TECHNOLOGY": tech,
                    "PLANT": plant,
                    "YEAR": year,
                    "GENERATION_MWH": round(metrics["generation_mwh"], 6),
                }
            )

        return {
            "technologies": technologies,
            "capacity_by_year": capacity_rows,
            "generation_by_year": generation_rows,
        }

    def from_model_outputs(self, outputs: dict[str, object]) -> Dataset:
        """Convert OSeMOSYS-derived outputs back into an OEI dataset.

        Args:
            outputs: A mapping containing ``capacity_by_year`` and
                ``generation_by_year`` rows produced by or for OSeMOSYS.

        Returns:
            An OEI ``Dataset`` with full provenance recorded.

        Raises:
            AdapterError: If the expected tables are absent.
        """
        capacity_rows = outputs.get("capacity_by_year")
        generation_rows = outputs.get("generation_by_year")
        if not isinstance(capacity_rows, list) or not isinstance(generation_rows, list):
            raise AdapterError(
                "Outputs must include capacity_by_year and generation_by_year lists."
            )

        merged: dict[tuple[str, str, int], dict[str, float]] = {}
        for row in capacity_rows:
            key = (str(row["PLANT"]), str(row["TECHNOLOGY"]), int(row["YEAR"]))
            merged.setdefault(key, {"capacity_mw": 0.0, "generation_mwh": 0.0})
            merged[key]["capacity_mw"] = float(row["CAPACITY_MW"])
        for row in generation_rows:
            key = (str(row["PLANT"]), str(row["TECHNOLOGY"]), int(row["YEAR"]))
            merged.setdefault(key, {"capacity_mw": 0.0, "generation_mwh": 0.0})
            merged[key]["generation_mwh"] = float(row["GENERATION_MWH"])

        records: list[DatasetRecord] = []
        for (plant, tech, year), metrics in sorted(merged.items()):
            records.append(
                DatasetRecord(
                    values={
                        "timestamp": f"{year}-01-01T00:00:00Z",
                        "plant_name": plant,
                        "technology": tech,
                        "capacity_mw": metrics["capacity_mw"],
                        "generation_mwh": metrics["generation_mwh"],
                    }
                )
            )

        provenance = Provenance(
            source_name="osemosys_outputs",
            source_uri="internal://osemosys/outputs",
            source_licence="Apache-2.0",
            source_hash="0" * 64,
        )
        provenance.add_step(
            operation="adapter.from_model_outputs",
            description="Converted OSeMOSYS capacity and generation tables into OEI records.",
            adapter=self.name,
            row_count=len(records),
        )

        return Dataset(
            name="osemosys_outputs",
            schema_fields=[
                FieldSpec(name="timestamp", type=FieldType.TIMESTAMP),
                FieldSpec(name="plant_name", type=FieldType.STRING),
                FieldSpec(name="technology", type=FieldType.CATEGORICAL),
                FieldSpec(name="capacity_mw", type=FieldType.FLOAT, unit="MW", minimum=0),
                FieldSpec(name="generation_mwh", type=FieldType.FLOAT, unit="MWh", minimum=0),
            ],
            records=records,
            provenance=provenance,
        )
