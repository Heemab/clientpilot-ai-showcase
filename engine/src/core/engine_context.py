"""
Shared execution context for the ClientPilot AI engine.

The EngineContext carries state through the entire workflow.
Each orchestration service reads from and writes to this object.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class EngineContext:
    """
    Shared execution context for a pipeline run.

    This object is passed through every orchestration service.
    Services should enrich the context instead of creating their own
    disconnected state.
    """

    # ------------------------------------------------------------------
    # Request Information
    # ------------------------------------------------------------------

    workspace_id: str | None = None
    website: str | None = None
    company_name: str | None = None

    # ------------------------------------------------------------------
    # Pipeline Outputs
    # ------------------------------------------------------------------

    audit_report: Any = None
    opportunity_score: Any = None
    proposal: Any = None
    outreach: Any = None
    dashboard: Any = None

    # ------------------------------------------------------------------
    # Shared Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    started_at: datetime = field(default_factory=datetime.utcnow)

    execution_log: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    def log(self, message: str) -> None:
        """Append a message to the execution log."""
        self.execution_log.append(message)

    def set_metadata(self, key: str, value: Any) -> None:
        """Store arbitrary metadata."""
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Retrieve metadata."""
        return self.metadata.get(key, default)