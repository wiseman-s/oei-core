"""Structured logging setup for OEI Core."""

from __future__ import annotations

import logging
import sys
from typing import Final

_FORMAT: Final[str] = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATEFMT: Final[str] = "%Y-%m-%dT%H:%M:%S%z"


def configure_logging(level: str = "INFO") -> None:
    """Configure the root logger for OEI processes.

    Args:
        level: Logging level name (e.g. ``"DEBUG"``, ``"INFO"``).
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt=_FORMAT, datefmt=_DATEFMT))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level.upper())


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger for an OEI module."""
    return logging.getLogger(f"oei.{name}")
