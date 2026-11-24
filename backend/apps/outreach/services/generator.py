from apps.outreach.models import Outreach
from apps.proposals.models import Proposal


def generate_outreach(proposal: Proposal) -> Outreach:
    """
    Generate personalized outreach messages from a proposal.

    If outreach already exists for this proposal,
    it will be updated with the latest proposal data.
    """

    if proposal is None:
        raise ValueError("Proposal is required.")

    lead = proposal.lead
    audit = proposal.audit

    opportunities = audit.opportunities or []

    services = []
    reasons = []

    for item in opportunities:
        service = item.get("service")
        reason = item.get("reason")

        if service:
            services.append(service)

        if reason:
            reasons.append(reason)

    service_text = (
        ", ".join(services)
        if services
        else "Website Improvements"
    )

    reason_text = (
        "\n• " + "\n• ".join(reasons)
        if reasons
        else "• Improve website performance and customer acquisition."
    )

    investment = proposal.estimated_value or 0
    hours = proposal.estimated_hours or 0

    subject = f"{lead.company_name}: {service_text}"

    cold_email = f"""Hello,

I recently reviewed {lead.company_name}'s website:

{lead.website}

While reviewing the site I identified several opportunities that could improve customer acquisition, search visibility and overall website performance.

Primary recommendations:

{reason_text}

Based on the assessment, these improvements have an estimated implementation value of ${investment} and approximately {hours} hours of work.

I've already prepared a detailed proposal outlining every recommendation.

If you'd like, I'd be happy to walk you through the findings and answer any questions.

Kind regards,
"""

    follow_up_1 = f"""Hello,

Just checking whether you had a chance to review the website proposal for {lead.company_name}.

The recommendations focus on:

{service_text}

I'd be happy to answer any questions or explain the recommendations in more detail.

Kind regards,
"""

    follow_up_2 = f"""Hello,

I wanted to send one final follow-up regarding the website review for {lead.company_name}.

Many businesses delay these improvements until traffic or enquiries begin to decline.

If you'd like to discuss the proposal, just reply to this email and I'll be happy to help.

Kind regards,
"""

    linkedin_message = (
        f"Hi, I recently reviewed {lead.company_name}'s website and noticed "
        f"opportunities around {service_text.lower()}. "
        f"I've prepared a short proposal and would be happy to share it."
    )

    whatsapp_message = (
        f"Hi! I reviewed {lead.company_name}'s website and found opportunities "
        f"around {service_text.lower()}. "
        f"The recommended improvements are valued at "
        f"${investment}. Happy to send the proposal if you're interested."
    )

    outreach, _ = Outreach.objects.update_or_create(
        proposal=proposal,
        defaults={
            "subject": subject,
            "cold_email": cold_email,
            "follow_up_1": follow_up_1,
            "follow_up_2": follow_up_2,
            "linkedin_message": linkedin_message,
            "whatsapp_message": whatsapp_message,
            "status": Outreach.STATUS_READY,
        },
    )

    return outreach