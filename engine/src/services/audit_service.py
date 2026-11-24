from __future__ import annotations

from src.audit.audit_context_builder import AuditContextBuilder
from src.audit.audit_package import AuditPackage
from src.models.audit_report import AuditReport
from src.models.opportunity import Opportunity


class AuditService:
    """
    Coordinates the complete website audit workflow.

    This service prepares the audit context, executes all
    registered audits, and returns a consolidated report.
    """

    def __init__(
        self,
        builder: AuditContextBuilder | None = None,
        package: AuditPackage | None = None,
    ) -> None:

        self._builder = builder or AuditContextBuilder()
        self._package = package or AuditPackage()

    def analyze(
        self,
        opportunity: Opportunity,
    ) -> AuditReport:

        context = self._builder.build(opportunity)

        return self._package.analyze(context)