"""Field-level validators used by the quality engine."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from oei.models.field import FieldSpec, FieldType
from oei.models.quality import QualityIssue, Severity


def validate_required(field: FieldSpec, value: Any, row_index: int) -> QualityIssue | None:
    if field.required and (value is None or value == ""):
        return QualityIssue(
            code="required_missing",
            message=f"Required field '{field.name}' is empty.",
            severity=Severity.ERROR,
            row_index=row_index,
            field_name=field.name,
        )
    return None


def validate_type(field: FieldSpec, value: Any, row_index: int) -> QualityIssue | None:
    if value is None:
        return None
    if field.type is FieldType.FLOAT:
        try:
            float(value)
        except (TypeError, ValueError):
            return QualityIssue(
                code="type_mismatch",
                message=f"Field '{field.name}' expected float, got {type(value).__name__}.",
                severity=Severity.ERROR,
                row_index=row_index,
                field_name=field.name,
            )
    elif field.type is FieldType.INTEGER:
        try:
            int(value)
        except (TypeError, ValueError):
            return QualityIssue(
                code="type_mismatch",
                message=f"Field '{field.name}' expected integer, got {type(value).__name__}.",
                severity=Severity.ERROR,
                row_index=row_index,
                field_name=field.name,
            )
    elif field.type is FieldType.TIMESTAMP:
        try:
            datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return QualityIssue(
                code="invalid_timestamp",
                message=f"Field '{field.name}' is not ISO-8601: {value!r}.",
                severity=Severity.ERROR,
                row_index=row_index,
                field_name=field.name,
            )
    return None


def validate_range(field: FieldSpec, value: Any, row_index: int) -> QualityIssue | None:
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if field.minimum is not None and numeric < field.minimum:
        return QualityIssue(
            code="below_minimum",
            message=f"Field '{field.name}' value {numeric} < {field.minimum}.",
            severity=Severity.WARNING,
            row_index=row_index,
            field_name=field.name,
        )
    if field.maximum is not None and numeric > field.maximum:
        return QualityIssue(
            code="above_maximum",
            message=f"Field '{field.name}' value {numeric} > {field.maximum}.",
            severity=Severity.WARNING,
            row_index=row_index,
            field_name=field.name,
        )
    return None


def validate_categorical(field: FieldSpec, value: Any, row_index: int) -> QualityIssue | None:
    if value is None or not field.allowed_values:
        return None
    if str(value) not in field.allowed_values:
        return QualityIssue(
            code="invalid_categorical",
            message=f"Field '{field.name}' value {value!r} not in allowed values.",
            severity=Severity.ERROR,
            row_index=row_index,
            field_name=field.name,
        )
    return None
