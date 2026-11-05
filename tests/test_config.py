"""Tests for runtime configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

from oei.config import Settings, load_settings, reset_settings_cache


def test_defaults() -> None:
    settings = Settings()
    assert settings.api_port == 8000
    assert settings.strict_validation is True
    assert settings.log_level == "INFO"


def test_env_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("OEI_API_PORT", "9000")
    monkeypatch.setenv("OEI_EXPORT_DIR", str(tmp_path / "exports"))
    monkeypatch.setenv("OEI_LOG_LEVEL", "debug")
    settings = Settings()
    assert settings.api_port == 9000
    assert settings.export_dir == tmp_path / "exports"
    assert settings.log_level == "DEBUG"


def test_cache_and_reset(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_settings_cache()
    monkeypatch.setenv("OEI_API_PORT", "8001")
    first = load_settings()
    second = load_settings()
    assert first is second
    assert first.api_port == 8001
    reset_settings_cache()
    third = load_settings()
    assert third is not first
