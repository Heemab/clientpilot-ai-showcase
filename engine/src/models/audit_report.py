"""
Aggregate report produced by AuditPackage.

An AuditReport combines the results of multiple audit modules
(e.g. SEO, Security) into a single report suitable for the
application layer and frontend.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.models.audit_result import AuditResult
from src.models.audit_finding import AuditFinding


@dataclass(slots=True)
class AuditReport:
    """
    Represents the complete audit of a website.
    """

    results: list[AuditResult] = field(default_factory=list)

    def add_result(self, result: AuditResult) -> None:
        self.results.append(result)

    @property
    def overall_score(self) -> int:
        if not self.results:
            return 0

        return round(
            sum(result.score for result in self.results)
            / len(self.results)
        )

    @property
    def findings(self) -> list[AuditFinding]:
        findings: list[AuditFinding] = []

        for result in self.results:
            findings.extend(result.findings)

        return findings

    @property
    def issue_count(self) -> int:
        return len(self.findings)

    @property
    def metrics(self) -> dict:
        merged: dict = {}

        for result in self.results:
            merged[result.name] = result.metrics

        return merged

    # ======================================================
    # Helper methods for Scoring, Proposal, Dashboard
    # ======================================================

    def result(self, name: str) -> AuditResult | None:
        """
        Return an audit result by name.
        """
        for result in self.results:
            if result.name == name:
                return result

        return None

    def has_result(self, name: str) -> bool:
        """
        Check whether an audit module exists.
        """
        return self.result(name) is not None

    def has_finding(self, title: str) -> bool:
        """
        Check whether a finding with the given title exists.
        """
        return any(f.title == title for f in self.findings)

    def findings_by_severity(
        self,
        severity: str,
    ) -> list[AuditFinding]:
        """
        Return findings matching a severity.
        """
        return [
            f
            for f in self.findings
            if f.severity.lower() == severity.lower()
        ]

    def findings_by_category(
        self,
        category: str,
    ) -> list[AuditFinding]:
        """
        Return findings belonging to a category.
        """
        return [
            f
            for f in self.findings
            if f.category.lower() == category.lower()
        ]