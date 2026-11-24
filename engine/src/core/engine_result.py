"""
Standard execution result for the ClientPilot AI engine.

Every orchestration service returns an EngineResult.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class EngineResult:
    """
    Represents the outcome of a service execution.

    A service should never return arbitrary dictionaries.
    Instead, it should return an EngineResult that provides
    a consistent contract across the entire engine.
    """

    success: bool = True

    data: Any = None

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    metrics: dict[str, Any] = field(default_factory=dict)

    def add_warning(self, message: str) -> None:
        """Record a warning."""
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        """Record an error."""
        self.errors.append(message)
        self.success = False

    def add_metric(self, name: str, value: Any) -> None:
        """Record execution metrics."""
        self.metrics[name] = value

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)