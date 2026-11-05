"""OEI Core: open energy data integration and validation engine."""

from oei.models.dataset import Dataset, DatasetRecord
from oei.models.field import FieldSpec, FieldType
from oei.models.provenance import Provenance
from oei.models.quality import QualityIssue, QualityReport, Severity

__all__ = [
    "Dataset",
    "DatasetRecord",
    "FieldSpec",
    "FieldType",
    "Provenance",
    "QualityIssue",
    "QualityReport",
    "Severity",
]

__version__ = "0.1.0"
