"""Quality reporting engine for OEI datasets."""

from __future__ import annotations

from oei.models.dataset import Dataset
from oei.models.quality import QualityReport
from oei.validation.validators import (
    validate_categorical,
    validate_range,
    validate_required,
    validate_type,
)


def build_quality_report(dataset: Dataset) -> QualityReport:
    """Validate every record against its field spec and aggregate a report."""
    report = QualityReport(dataset_name=dataset.name, total_rows=len(dataset.records))
    field_index = {f.name: f for f in dataset.schema_fields}

    for row_index, record in enumerate(dataset.records):
        for field_name, spec in field_index.items():
            value = record.values.get(field_name)
            for validator in (
                validate_required,
                validate_type,
                validate_range,
                validate_categorical,
            ):
                issue = validator(spec, value, row_index)
                if issue is not None:
                    report.issues.append(issue)
    return report
