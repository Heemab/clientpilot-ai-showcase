from dataclasses import dataclass, field
from typing import List


@dataclass
class OpportunityReport:
    """
    Complete intelligence report for an opportunity.

    This object acts as the bridge between
    opportunity discovery and client outreach.
    """

    # -------------------------
    # Business Information
    # -------------------------

    business_name: str

    category: str

    website: str

    technology: str

    priority: str

    # -------------------------
    # Opportunity
    # -------------------------

    opportunity_score: int

    # -------------------------
    # Intelligence
    # -------------------------

    problems: List[str] = field(default_factory=list)

    recommended_services: List[str] = field(default_factory=list)

    primary_service: str = ""

    # -------------------------
    # Sales Intelligence
    # -------------------------

    estimated_value: str = ""

    estimated_difficulty: str = ""

    pitch_angle: str = ""

    notes: str = ""