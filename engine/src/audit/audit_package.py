from __future__ import annotations

from collections.abc import Iterable

from src.audit.base_audit import BaseAudit
from src.audit.seo_audit import SEOAudit
from src.audit.security_audit import SecurityAudit

from src.models.audit_context import AuditContext
from src.models.audit_report import AuditReport


class AuditPackage:
    """
    Public interface for the audit subsystem.

    Executes all registered audits and returns a
    consolidated AuditReport.
    """

    def __init__(
        self,
        audits: Iterable[BaseAudit] | None = None,
    ):

        self._audits: list[BaseAudit] = (

            list(audits)

            if audits

            else [

                SEOAudit(),

                SecurityAudit(),

            ]

        )

    def analyze(
        self,
        context: AuditContext,
    ) -> AuditReport:
        """
        Execute every registered audit.
        """

        report = AuditReport()

        for audit in self._audits:

            report.add_result(

                audit.analyze(context)

            )

        return report

    def register(
        self,
        audit: BaseAudit,
    ):
        """
        Register a new audit module.
        """

        self._audits.append(
            audit
        )