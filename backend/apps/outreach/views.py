from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.proposals.models import Proposal

from .models import Outreach, OutreachEvent
from .services.email_sender import EmailSender
from .services.generator import generate_outreach
from .services.timeline import TimelineService


@login_required
def list_outreach(request):
    """
    Outreach dashboard with optional status filter.
    """

    status = request.GET.get("status")

    outreach_list = (
        Outreach.objects.select_related(
            "proposal",
            "proposal__lead",
        )
        .filter(
            proposal__lead__organization=request.user.organization
        )
    )

    if status:
        outreach_list = outreach_list.filter(status=status)

    outreach_list = outreach_list.order_by("-created_at")

    return render(
        request,
        "outreach/list.html",
        {
            "outreach_list": outreach_list,
            "current_status": status,
            "statuses": Outreach.STATUS_CHOICES,
        },
    )


@login_required
@require_POST
def generate(request, proposal_id):
    """
    Generate outreach for a proposal.
    """

    proposal = get_object_or_404(
        Proposal.objects.select_related(
            "lead",
        ),
        pk=proposal_id,
        lead__organization=request.user.organization,
    )

    outreach = Outreach.objects.filter(
        proposal=proposal,
    ).first()

    if outreach is None:

        outreach = generate_outreach(proposal)

        TimelineService.log(
            outreach=outreach,
            event_type=OutreachEvent.EVENT_GENERATED,
            user=request.user,
        )

    return redirect(
        "outreach:outreach_detail",
        outreach_id=outreach.id,
    )


@login_required
def detail(request, outreach_id):
    """
    Display and edit an outreach package.
    """

    outreach = get_object_or_404(
        Outreach.objects.select_related(
            "proposal",
            "proposal__lead",
        ),
        pk=outreach_id,
        proposal__lead__organization=request.user.organization,
    )

    if request.method == "POST":

        outreach.subject = request.POST.get(
            "subject",
            outreach.subject,
        )

        outreach.cold_email = request.POST.get(
            "cold_email",
            outreach.cold_email,
        )

        outreach.save(
            update_fields=[
                "subject",
                "cold_email",
            ]
        )

        TimelineService.log(
            outreach=outreach,
            event_type=OutreachEvent.EVENT_DRAFT_SAVED,
            user=request.user,
        )

        messages.success(
            request,
            "Draft saved successfully.",
        )

        return redirect(
            "outreach:outreach_detail",
            outreach_id=outreach.id,
        )

    return render(
        request,
        "outreach/detail.html",
        {
            "outreach": outreach,
        },
    )


@login_required
@require_POST
def send_email(request, outreach_id):
    """
    Save latest edits and send outreach email.
    """

    outreach = get_object_or_404(
        Outreach.objects.select_related(
            "proposal",
            "proposal__lead",
        ),
        pk=outreach_id,
        proposal__lead__organization=request.user.organization,
    )

    outreach.subject = request.POST.get(
        "subject",
        outreach.subject,
    )

    outreach.cold_email = request.POST.get(
        "cold_email",
        outreach.cold_email,
    )

    outreach.save(
        update_fields=[
            "subject",
            "cold_email",
        ]
    )

    try:

        EmailSender.send(outreach)

        outreach.status = Outreach.STATUS_SENT

        outreach.save(
            update_fields=[
                "status",
            ]
        )

        TimelineService.log(
            outreach=outreach,
            event_type=OutreachEvent.EVENT_EMAIL_SENT,
            user=request.user,
        )

        messages.success(
            request,
            f"Email sent successfully to {outreach.proposal.lead.email}.",
        )

    except Exception as exc:

        messages.error(
            request,
            str(exc),
        )

    return redirect(
        "outreach:outreach_detail",
        outreach_id=outreach.id,
    )


@login_required
@require_POST
def update_status(request, outreach_id, status):
    """
    Update the outreach status.
    """

    outreach = get_object_or_404(
        Outreach.objects.select_related(
            "proposal",
            "proposal__lead",
        ),
        pk=outreach_id,
        proposal__lead__organization=request.user.organization,
    )

    valid_statuses = dict(Outreach.STATUS_CHOICES)

    if status in valid_statuses:

        outreach.status = status

        outreach.save(
            update_fields=[
                "status",
            ]
        )

        event_map = {
            Outreach.STATUS_OPENED: OutreachEvent.EVENT_OPENED,
            Outreach.STATUS_REPLIED: OutreachEvent.EVENT_REPLIED,
            Outreach.STATUS_MEETING: OutreachEvent.EVENT_MEETING,
            Outreach.STATUS_WON: OutreachEvent.EVENT_WON,
            Outreach.STATUS_LOST: OutreachEvent.EVENT_LOST,
        }

        if status in event_map:
            TimelineService.log(
                outreach=outreach,
                event_type=event_map[status],
                user=request.user,
            )

    return redirect("outreach:outreach_list")