from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.outreach.models import Outreach
from apps.proposals.models import Proposal

from .forms import LeadForm, LeadTaskForm
from .models import Lead, LeadTask
from .services.lead_pipeline_service import LeadPipelineService


@login_required
def lead_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "-created_at")

    leads = (
        Lead.objects.filter(
            organization=request.user.organization
        )
        .prefetch_related(
            "audits",
            "proposals__outreach",
        )
    )

    if query:
        leads = leads.filter(
            Q(company_name__icontains=query)
            | Q(contact_name__icontains=query)
            | Q(email__icontains=query)
            | Q(website__icontains=query)
        )

    if status:
        leads = leads.filter(status=status)

    allowed_sort_fields = [
        "company_name",
        "-company_name",
        "status",
        "-status",
        "priority",
        "-priority",
        "created_at",
        "-created_at",
    ]

    if sort not in allowed_sort_fields:
        sort = "-created_at"

    leads = leads.order_by(sort)

    paginator = Paginator(leads, 20)

    page_number = request.GET.get("page")

    leads = paginator.get_page(page_number)

    return render(
        request,
        "leads/list.html",
        {
            "leads": leads,
            "query": query,
            "status": status,
            "sort": sort,
        },
    )


@login_required
def lead_create(request):
    if request.method == "POST":
        form = LeadForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            lead = form.save(commit=False)
            lead.organization = request.user.organization
            lead.assigned_to = request.user
            lead.save()

            return redirect("leads:list")

    else:
        form = LeadForm(user=request.user)

    return render(
        request,
        "leads/form.html",
        {
            "form": form,
            "title": "Create Lead",
        },
    )


@login_required
def lead_detail(request, pk):
    """
    Lead 360 Dashboard
    """

    lead = get_object_or_404(
        Lead.objects.prefetch_related(
            "audits",
            "tasks__assigned_to",
            Prefetch(
                "proposals",
                queryset=Proposal.objects.prefetch_related(
                    "outreach__events"
                ).order_by("-created_at"),
            ),
        ),
        pk=pk,
        organization=request.user.organization,
    )

    audits = lead.audits.all().order_by("-created_at")

    proposals = lead.proposals.all().order_by("-created_at")

    tasks = lead.tasks.select_related(
    "assigned_to").order_by("status", "due_date", "-created_at")

    latest_proposal = proposals.first()

    latest_outreach = None

    outreach_history = []

    timeline = []

    if latest_proposal:
        latest_outreach = getattr(
            latest_proposal,
            "outreach",
            None,
        )

    for proposal in proposals:

        outreach = getattr(
            proposal,
            "outreach",
            None,
        )

        if outreach:

            outreach_history.append(outreach)

            timeline.extend(
                outreach.events.all()
            )

    timeline.sort(
        key=lambda e: e.created_at,
        reverse=True,
    )

    return render(
        request,
        "leads/detail.html",
        {
            "lead": lead,
            "audits": audits,
            "proposals": proposals,
            "latest_proposal": latest_proposal,
            "latest_outreach": latest_outreach,
            "outreach_history": outreach_history,
            "timeline": timeline,
            "tasks": tasks,
        },
    )


@require_POST
@login_required
def run_pipeline(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
        organization=request.user.organization,
    )

    pipeline = LeadPipelineService()

    result = pipeline.run(lead)

    for step in result.steps_completed:
        messages.success(
            request,
            f"✓ {step}",
        )

    for warning in result.warnings:
        messages.warning(
            request,
            warning,
        )

    for error in result.errors:
        messages.error(
            request,
            error,
        )

    return redirect(
        "leads:lead_detail",
        pk=lead.pk,
    )


@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
        organization=request.user.organization,
    )

    if request.method == "POST":

        form = LeadForm(
            request.POST,
            instance=lead,
            user=request.user,
        )

        if form.is_valid():

            lead = form.save(commit=False)

            lead.organization = request.user.organization

            lead.assigned_to = request.user

            lead.save()

            return redirect(
                "leads:lead_detail",
                pk=lead.pk,
            )

    else:

        form = LeadForm(
            instance=lead,
            user=request.user,
        )

    return render(
        request,
        "leads/form.html",
        {
            "form": form,
            "title": "Edit Lead",
        },
    )

@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
        organization=request.user.organization,
    )

    if request.method == "POST":

        lead.delete()

        return redirect(
            "leads:list",
        )

    return render(
        request,
        "leads/delete.html",
        {
            "lead": lead,
        },
    )

@login_required
def task_create(request, pk):
    lead = get_object_or_404(
        Lead,
        pk=pk,
        organization=request.user.organization,
    )

    if request.method == "POST":
        form = LeadTaskForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            task = form.save(commit=False)
            task.lead = lead

            if not task.assigned_to:
                task.assigned_to = request.user

            task.save()

            messages.success(
                request,
                "Task created successfully.",
            )

            return redirect(
                "leads:lead_detail",
                pk=lead.pk,
            )

    else:
        form = LeadTaskForm(user=request.user)

    return render(
        request,
        "leads/task_form.html",
        {
            "form": form,
            "lead": lead,
            "title": "Create Task",
        },
    )


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(
        LeadTask.objects.select_related("lead"),
        pk=task_id,
        lead__organization=request.user.organization,
    )

    if request.method == "POST":
        form = LeadTaskForm(
            request.POST,
            instance=task,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task updated successfully.",
            )

            return redirect(
                "leads:lead_detail",
                pk=task.lead.pk,
            )

    else:
        form = LeadTaskForm(
            instance=task,
            user=request.user,
        )

    return render(
        request,
        "leads/task_form.html",
        {
            "form": form,
            "lead": task.lead,
            "task": task,
            "title": "Edit Task",
        },
    )


@require_POST
@login_required
def task_complete(request, task_id):
        task = get_object_or_404(
            LeadTask.objects.select_related("lead"),
            pk=task_id,
            lead__organization=request.user.organization,
        )

        task.mark_completed()

        messages.success(
            request,
            "Task completed.",
        )

        return redirect(
            "leads:lead_detail",
            pk=task.lead.pk,
        )


@require_POST
@login_required
def task_delete(request, task_id):
        task = get_object_or_404(
            LeadTask.objects.select_related("lead"),
            pk=task_id,
            lead__organization=request.user.organization,
        )

        lead_pk = task.lead.pk

        task.delete()

        messages.success(
            request,
            "Task deleted.",
        )

        return redirect(
            "leads:lead_detail",
            pk=lead_pk,
        )