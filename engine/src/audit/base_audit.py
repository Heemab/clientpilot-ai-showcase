from abc import ABC, abstractmethod

from src.models.audit_context import AuditContext
from src.models.audit_result import AuditResult


class BaseAudit(ABC):
    """
    Base class for all audit modules.
    """

    name = "Base Audit"

    @abstractmethod
    def analyze(
        self,
        context: AuditContext,
    ) -> AuditResult:
        """
        Execute an audit.

        Returns an AuditResult.
        """

        raise NotImplementedError