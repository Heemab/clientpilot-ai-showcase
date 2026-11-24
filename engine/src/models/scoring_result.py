from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ScoringResult:
    """
    Final scoring outcome for an opportunity.
    """

    score: int

    grade: str

    priority: str

    confidence: int

    estimated_revenue: float

    recommended_services: list[str] = field(default_factory=list)

    reasoning: list[str] = field(default_factory=list)

    metrics: dict[str, Any] = field(default_factory=dict)