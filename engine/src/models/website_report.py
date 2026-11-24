from dataclasses import dataclass

from src.models.audit_result import AuditResult


@dataclass(slots=True)
class WebsiteReport:
    """
    Complete website assessment.

    Future versions will continue expanding this
    model while keeping a stable interface.
    """

    url: str

    technology: str = "Unknown"

    security: AuditResult | None = None

    seo: AuditResult | None = None

    ux: AuditResult | None = None

    trust: AuditResult | None = None

    performance: AuditResult | None = None

    marketing: AuditResult | None = None

    overall_score: int = 0