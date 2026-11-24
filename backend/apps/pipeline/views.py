from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.leads.models import Lead


@login_required
def index(request):
    leads = (
        Lead.objects.filter(
            organization=request.user.organization
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "pipeline/index.html",
        {
            "leads": leads,
        },
    )