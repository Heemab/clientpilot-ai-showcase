from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.audits.models import Audit
from apps.proposals.models import Proposal
from apps.proposals.services.builder import build_proposal
from apps.proposals.utils import render_to_pdf


@login_required
def proposal_list(request):
    """
    Display all proposals for the current organization.
    """

    proposals = (
        Proposal.objects.select_related("lead")
        .filter(
            lead__organization=request.user.organization
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "proposals/list.html",
        {
            "proposals": proposals,
        },
    )


@login_required
@require_POST
def generate_proposal(request, audit_id):
    """
    Generate a proposal from an audit.
    """

    audit = get_object_or_404(
        Audit.objects.select_related("lead"),
        pk=audit_id,
        lead__organization=request.user.organization,
    )

    try:
        proposal = audit.proposal
    except Proposal.DoesNotExist:
        proposal = build_proposal(audit)

    return redirect(
        "proposals:proposal_detail",
        proposal_id=proposal.id,
    )


@login_required
def proposal_detail(request, proposal_id):
    """
    Display a proposal.
    """

    proposal = get_object_or_404(
        Proposal.objects.select_related("lead"),
        pk=proposal_id,
        lead__organization=request.user.organization,
    )

    return render(
        request,
        "proposals/detail.html",
        {
            "proposal": proposal,
        },
    )


@login_required
def proposal_pdf(request, proposal_id):
    """
    Download proposal PDF.
    """

    proposal = get_object_or_404(
        Proposal.objects.select_related("lead"),
        pk=proposal_id,
        lead__organization=request.user.organization,
    )

    response = render_to_pdf(
        "proposals/pdf.html",
        {
            "proposal": proposal,
        },
    )

    if response:
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{proposal.proposal_number}.pdf"'

    return response