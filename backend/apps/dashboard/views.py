from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.leads.models import Lead
from apps.audits.models import Audit
from apps.proposals.models import Proposal
from apps.outreach.models import Outreach


@login_required
def dashboard(request):
    leads = Lead.objects.filter(
        organization=request.user.organization
    )

    audits = Audit.objects.filter(
        lead__organization=request.user.organization
    )

    proposals = Proposal.objects.filter(
        lead__organization=request.user.organization
    )

    outreach = Outreach.objects.filter(
        proposal__lead__organization=request.user.organization
    )

    # Demo statistics if the account has no data
    lead_count = leads.count()

    context = {
        "total_leads": lead_count if lead_count else 36,
        "new_leads": leads.filter(status="new").count() if lead_count else 12,
        "qualified_leads": leads.filter(status="qualified").count() if lead_count else 15,
        "won_leads": leads.filter(status="won").count() if lead_count else 7,
        "lost_leads": leads.filter(status="lost").count() if lead_count else 2,

        "total_audits": audits.count() if audits.exists() else 14,
        "total_proposals": proposals.count() if proposals.exists() else 6,
        "total_outreach": outreach.count() if outreach.exists() else 22,

        "recent_leads": leads.order_by("-created_at")[:5],
        "demo_mode": lead_count == 0,
    }

    return render(
        request,
        "dashboard/index.html",
        context,
    )