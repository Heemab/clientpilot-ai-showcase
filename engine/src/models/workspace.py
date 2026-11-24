from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.models.opportunity import Opportunity


@dataclass(slots=True)
class Workspace:
    """
    Represents a fully reconstructed client workspace.

    This is the primary object returned by WorkspaceRepository.
    """

    id: int
    opportunity: Opportunity

    metadata: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)