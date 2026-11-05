"""Quality reporting primitives."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity levels for quality issues."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class QualityIssue(BaseModel):
    """A single data quality issue tied to a record and field."""

    code: str
    message: str
    severity: Severity
    row_index: int | None = None
    field_name: str | None = None


class QualityReport(BaseModel):
    """Aggregated quality report for a dataset."""

    dataset_name: str
    total_rows: int
    issues: list[QualityIssue] = Field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity is Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity is Severity.WARNING)

    @property
    def info_count(self) -> int:
        return sum(1 for i in self.issues if i.severity is Severity.INFO)

    @property
    def is_valid(self) -> bool:
        return self.error_count == 0
