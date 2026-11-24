from dataclasses import dataclass, field

from src.models.audit_finding import AuditFinding


@dataclass(slots=True)
class BusinessAssessment:
    """
    Represents the commercial assessment of a business.

    This object bridges the technical audit layer
    (WebsiteReport) and the commercial layer
    (Proposal, CRM, Outreach, Dashboard).

    It should contain everything required to make
    business decisions without re-reading the audit.
    """

    # --------------------------------------------------
    # Overall Assessment
    # --------------------------------------------------

    overall_score: int = 0

    priority: str = "MEDIUM"

    summary: str = ""

    # --------------------------------------------------
    # Commercial Recommendation
    # --------------------------------------------------

    recommended_services: list[str] = field(
        default_factory=list
    )

    primary_service: str = ""

    estimated_value: int = 0

    estimated_hours: int = 0

    difficulty: str = "Medium"

    roi_score: int = 0

    closing_probability: int = 0

    # --------------------------------------------------
    # Technical Findings
    # --------------------------------------------------

    findings: list[AuditFinding] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Proposal-ready Opportunities
    # --------------------------------------------------

    business_opportunities: list[dict] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Convenience Helpers
    # --------------------------------------------------

    @property
    def total_findings(self) -> int:

        return len(self.findings)

    @property
    def has_findings(self) -> bool:

        return len(self.findings) > 0

    @property
    def critical_findings(self) -> list[AuditFinding]:

        return [

            finding

            for finding in self.findings

            if finding.severity.lower() == "critical"

        ]

    @property
    def high_findings(self) -> list[AuditFinding]:

        return [

            finding

            for finding in self.findings

            if finding.severity.lower() == "high"

        ]

    @property
    def estimated_profit(self) -> int:
        """
        Simple helper for future reporting.
        """

        return self.estimated_value