"""
Base service contract for all orchestration services.

Every engine service should inherit from EngineService and implement
the execute() method.

Examples:
    AuditEngine
    ScoringEngine
    ProposalEngine
    OutreachEngine
    DashboardEngine
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.engine_context import EngineContext
    from src.core.engine_result import EngineResult


logger = logging.getLogger(__name__)


class EngineService(ABC):
    """
    Abstract base class for all orchestration services.

    Each service receives an EngineContext and returns an EngineResult.
    Services should avoid mutating external state directly and instead
    update the provided context or use repositories where appropriate.
    """

    @property
    def service_name(self) -> str:
        """Return the human-readable service name."""
        return self.__class__.__name__

    def before_execute(self, context: "EngineContext") -> None:
        """
        Hook executed immediately before the service runs.
        Override if a service needs setup logic.
        """
        logger.debug("%s starting.", self.service_name)

    @abstractmethod
    def execute(self, context: "EngineContext") -> "EngineResult":
        """
        Execute the service.

        Args:
            context: Shared pipeline execution context.

        Returns:
            EngineResult describing the outcome.
        """
        raise NotImplementedError

    def after_execute(
        self,
        context: "EngineContext",
        result: "EngineResult",
    ) -> None:
        """
        Hook executed immediately after the service completes.
        Override if cleanup or metrics collection is needed.
        """
        logger.debug("%s completed.", self.service_name)