"""Deterministic column transforms referenced by mapping configurations.

Transforms are pure functions with a stable ``name`` so that mapping files
can reference them by identifier and provenance can record exactly which
transform was applied.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from oei.errors import MappingError


def _year_to_iso(value: object) -> str:
    """Convert a four-digit year into an ISO 8601 timestamp."""
    text = str(value).strip()

    if len(text) != 4 or not text.isdigit():
        raise MappingError(f"year_to_iso expected a 4-digit year, got {value!r}")

    return f"{text}-01-01T00:00:00Z"


def _gwh_to_mwh(value: object) -> float:
    """Convert gigawatt-hours to megawatt-hours."""
    if isinstance(value, (int, float, str)):
        try:
            return float(value) * 1000.0
        except ValueError as exc:
            raise MappingError(f"gwh_to_mwh expected numeric input, got {value!r}") from exc

    raise MappingError(f"gwh_to_mwh expected numeric input, got {type(value).__name__}")


@dataclass(frozen=True)
class Transform:
    """A named pure function usable from mapping configurations."""

    name: str
    func: Callable[[object], object]


BUILTIN_TRANSFORMS: Final[dict[str, Transform]] = {
    transform.name: transform
    for transform in (
        Transform(name="year_to_iso", func=_year_to_iso),
        Transform(name="gwh_to_mwh", func=_gwh_to_mwh),
    )
}


def resolve_transform(name: str) -> Transform:
    """Return the transform registered under the given name.

    Args:
        name: Registered transform identifier.

    Returns:
        The matching Transform instance.

    Raises:
        MappingError: If no transform is registered under that name.
    """
    try:
        return BUILTIN_TRANSFORMS[name]
    except KeyError as exc:
        raise MappingError(f"Unknown transform: {name}") from exc
