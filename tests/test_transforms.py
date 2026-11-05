"""Tests for mapping transforms."""

from __future__ import annotations

import pytest

from oei.errors import MappingError
from oei.mapping.transforms import BUILTIN_TRANSFORMS, resolve_transform


def test_year_to_iso() -> None:
    transform = resolve_transform("year_to_iso")
    assert transform.func("2024") == "2024-01-01T00:00:00Z"


def test_year_to_iso_rejects_bad_input() -> None:
    transform = resolve_transform("year_to_iso")
    with pytest.raises(MappingError):
        transform.func("24")


def test_gwh_to_mwh() -> None:
    transform = resolve_transform("gwh_to_mwh")
    assert transform.func(1.5) == 1500.0


def test_unknown_transform() -> None:
    with pytest.raises(MappingError):
        resolve_transform("does_not_exist")


def test_builtin_registry_is_stable() -> None:
    assert set(BUILTIN_TRANSFORMS) == {"year_to_iso", "gwh_to_mwh"}
