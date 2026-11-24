from dataclasses import dataclass, field
from typing import List
import logging


logger = logging.getLogger(__name__)

from ..models import Lead
from .contact_intelligence import ContactIntelligence

@dataclass(slots=True)
class PipelineResult:
    success: bool = True
    steps_completed: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def add_step(self, step: str) -> None:
        self.steps_completed.append(step)

    def add_warning(self, warning: str) -> None:
        self.warnings.append(warning)

    def add_error(self, error: str) -> None:
        self.errors.append(error)
        self.success = False


class LeadPipelineService:
    """
    Coordinates every stage of lead processing.
    """

    def run(self, lead: Lead) -> PipelineResult:
        result = PipelineResult()

        try:
            if not lead.website:
                result.add_warning(
                    "Lead has no website. Contact Intelligence skipped."
                )
                return result

            # Future implementation
            # contact_info = ContactIntelligence().discover(lead)
            # self._update_lead(lead, contact_info)

            result.add_step("Pipeline initialized")
            contact = ContactIntelligence().discover(lead)

            if contact.business_email and not lead.email:
                lead.email = contact.business_email

            result.add_step("Contact Intelligence")

            lead.save()

        except Exception as exc:
            logger.exception("Lead pipeline failed")

            result.add_error(str(exc))

        return result