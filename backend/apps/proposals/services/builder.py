from django.utils import timezone

from apps.audits.models import Audit
from apps.proposals.models import Proposal


def generate_proposal_number():
    """
    Generate a proposal number.

    Example:
    PROP-20260722-153045
    """
    return timezone.now().strftime("PROP-%Y%m%d-%H%M%S")


def build_proposal(audit: Audit) -> Proposal:
    """
    Build a proposal from an audit.

    If one already exists, return the existing proposal.
    """

    if audit is None:
        raise ValueError("Audit is required to generate a proposal.")

    proposal, created = Proposal.objects.get_or_create(
        audit=audit,
        defaults={
            "proposal_number": generate_proposal_number(),
            "lead": audit.lead,
            "executive_summary": audit.executive_summary or "",
            "estimated_hours": audit.estimated_project_hours or 0,
            "estimated_timeline": getattr(
                audit,
                "estimated_timeline",
                "",
            ),
            "estimated_value": audit.estimated_project_value or 0,
            "terms": (
                "Payment due upon project completion "
                "unless otherwise agreed."
            ),
            "notes": "",
        },
    )

    # Ensure the proposal is always linked to the correct lead.
    if proposal.lead_id != audit.lead_id:
        proposal.lead = audit.lead
        proposal.save(update_fields=["lead"])

    return proposal