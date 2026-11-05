"""Exception hierarchy for OEI Core."""

from __future__ import annotations


class OEIError(Exception):
    """Base class for all OEI Core errors."""


class ConfigurationError(OEIError):
    """Raised when configuration is invalid or incomplete."""


class MappingError(OEIError):
    """Raised when a mapping configuration cannot be applied."""


class ValidationError(OEIError):
    """Raised when a dataset fails structural validation."""


class IOError(OEIError):
    """Raised when reading or writing a dataset fails."""


class AdapterError(OEIError):
    """Raised by model adapters when conversion fails."""
