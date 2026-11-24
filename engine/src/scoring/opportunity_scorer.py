from __future__ import annotations

from src.models.audit_report import AuditReport
from src.models.scoring_result import ScoringResult


class OpportunityScorer:
    """
    Calculates a Business Opportunity Score.

    Higher score = Better sales opportunity.
    """

    SERVICE_VALUES = {
        "Website Redesign": 2500,
        "SEO Optimization": 1200,
        "SSL Setup": 300,
        "Lead Generation Form": 600,
    }

    def score(
        self,
        opportunity,
        audit_report: AuditReport,
    ) -> ScoringResult:

        reasoning: list[str] = []
        services: list[str] = []

        website_score = self._website_health(
            audit_report,
            reasoning,
            services,
        )

        growth_score = self._business_growth(
            opportunity,
            reasoning,
        )

        technology_score = self._technology(
            audit_report,
            reasoning,
            services,
        )

        reputation_score = self._business_reputation(
            opportunity,
            reasoning,
        )

        total_score = min(
            website_score
            + growth_score
            + technology_score
            + reputation_score,
            100,
        )

        estimated_revenue = sum(
            self.SERVICE_VALUES.get(service, 0)
            for service in services
        )

        return ScoringResult(
            score=total_score,
            grade=self._grade(total_score),
            priority=self._priority(total_score),
            confidence=self._confidence(audit_report),
            estimated_revenue=estimated_revenue,
            recommended_services=sorted(set(services)),
            reasoning=reasoning,
            metrics={
                "website_health": website_score,
                "growth": growth_score,
                "technology": technology_score,
                "reputation": reputation_score,
            },
        )

    def _website_health(
        self,
        report: AuditReport,
        reasoning: list[str],
        services: list[str],
    ) -> int:

        score = 0

        if report.has_finding("No Business Email Detected"):
            score += 5
            reasoning.append("Website has no business email.")
            services.append("Lead Generation Form")

        if report.has_finding("No Contact Form Detected"):
            score += 5
            reasoning.append("Website has no contact form.")
            services.append("Lead Generation Form")

        if report.has_finding("No Business Email Detected"):
            score += 5
            reasoning.append("Website has no business email.")

        return score

    def _business_growth(
        self,
        opportunity,
        reasoning: list[str],
    ) -> int:

        reviews = getattr(opportunity, "reviews", 0) or 0

        if reviews <= 20:
            reasoning.append(
                "Business has very few reviews, indicating high growth potential."
            )
            return 30

        if reviews <= 50:
            reasoning.append(
                "Business is still in an early growth stage."
            )
            return 25

        if reviews <= 100:
            return 20

        if reviews <= 250:
            return 10

        if reviews <= 500:
            return 5

        return 0

    def _technology(
        self,
        report: AuditReport,
        reasoning: list[str],
        services: list[str],
    ) -> int:

        seo_metrics = report.metrics.get("SEO Audit", {})
        technology = seo_metrics.get("technology", "Unknown")

        if technology in ("Unknown", "Custom / Unknown"):
            reasoning.append(
                "Unknown technology stack presents modernization opportunities."
            )
            services.append("Website Redesign")
            return 20

        if technology == "Wix":
            reasoning.append(
                "Website is built with Wix and may benefit from a redesign."
            )
            services.append("Website Redesign")
            return 15

        if technology == "WordPress":
            reasoning.append(
                "WordPress website may benefit from SEO optimization."
            )
            services.append("SEO Optimization")
            return 8

        if technology == "Shopify":
            reasoning.append(
                "Shopify store may benefit from SEO optimization."
            )
            services.append("SEO Optimization")
            return 6

        return 0

    def _business_reputation(
        self,
        opportunity,
        reasoning: list[str],
    ) -> int:

        rating = getattr(opportunity, "rating", 0.0) or 0.0

        if rating < 4.0:
            reasoning.append(
                "Customer rating indicates an opportunity to improve reputation."
            )
            return 10

        if rating < 4.5:
            return 5

        return 0

    def _grade(
        self,
        score: int,
    ) -> str:

        if score >= 90:
            return "A+"

        if score >= 80:
            return "A"

        if score >= 70:
            return "B"

        if score >= 60:
            return "C"

        return "D"

    def _priority(
        self,
        score: int,
    ) -> str:

        if score >= 90:
            return "Critical"

        if score >= 75:
            return "High"

        if score >= 50:
            return "Medium"

        return "Low"

    def _confidence(
        self,
        report: AuditReport,
    ) -> int:

        confidence = 50

        if report.results:
            confidence += 30

        if report.metrics:
            confidence += 20

        return min(confidence, 100)