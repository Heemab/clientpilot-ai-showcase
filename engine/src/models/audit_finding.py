from dataclasses import dataclass


@dataclass(slots=True)
class AuditFinding:
    """
    Represents a single issue discovered during a website audit.
    """

    category: str

    severity: str

    title: str

    description: str

    business_impact: str

    recommendation: str

    effort_hours: float = 0.0

    estimated_value: int = 0