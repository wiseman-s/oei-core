"""Runtime configuration for OEI Core, loaded from environment and ``.env``."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven runtime settings.

    Values are read from environment variables prefixed with ``OEI_`` and
    from an optional ``.env`` file in the working directory.
    """

    model_config = SettingsConfigDict(
        env_prefix="OEI_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    data_dir: Path = Field(default=Path("./data"))
    export_dir: Path = Field(default=Path("./exports"))
    log_level: str = Field(default="INFO")
    api_host: str = Field(default="127.0.0.1")
    api_port: int = Field(default=8000, ge=1, le=65535)
    strict_validation: bool = Field(default=True)
    max_preview_rows: int = Field(default=50, ge=1, le=1000)
    provenance_schema_version: str = Field(default="0.1.0")

    @field_validator("log_level")
    @classmethod
    def _upper_log_level(cls, value: str) -> str:
        return value.upper()

    @field_validator("data_dir", "export_dir")
    @classmethod
    def _expand_user(cls, value: Path) -> Path:
        return value.expanduser()


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    """Return a cached ``Settings`` instance.

    The cache makes configuration cheap to consume across CLI, API and
    library call sites while remaining overridable in tests via
    ``load_settings.cache_clear()``.
    """
    return Settings()


def reset_settings_cache() -> None:
    """Clear the settings cache; useful for tests and reload scenarios."""
    load_settings.cache_clear()
