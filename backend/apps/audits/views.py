from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.leads.models import Lead

from .models import Audit
from .services import WebsiteAuditService


@login_required
def audit_list(request):
    """
    Display all audits for the current user's organization.
    """

    audits = (
        Audit.objects.filter(
            lead__organization=request.user.organization
        )
        .select_related("lead")
        .order_by("-created_at")
    )

    return render(
        request,
        "audits/list.html",
        {
            "audits": audits,
        },
    )


@login_required
def audit_detail(request, pk):
    """
    Display a single audit report.
    """

    audit = get_object_or_404(
        Audit.objects.select_related("lead"),
        pk=pk,
        lead__organization=request.user.organization,
    )

    # Proposal generated from this audit (if any)
    proposal = getattr(audit, "proposal", None)

    # Outreach generated from the proposal (if any)
    outreach = None

    if proposal:
        outreach = getattr(
            proposal,
            "outreach",
            None,
        )

    return render(
        request,
        "audits/detail.html",
        {
            "audit": audit,
            "proposal": proposal,
            "outreach": outreach,
        },
    )


@login_required
@require_POST
def run_audit(request, lead_id):
    """
    Run a website audit and save the results.
    """

    lead = get_object_or_404(
        Lead,
        pk=lead_id,
        organization=request.user.organization,
    )

    results = WebsiteAuditService.run(lead.website)

    audit = Audit.objects.create(

        # -------------------------------------------------
        # Lead
        # -------------------------------------------------

        lead=lead,
        website=results["website"],

        # -------------------------------------------------
        # Security
        # -------------------------------------------------

        ssl_enabled=results["ssl_enabled"],
        https_redirect=results["https_redirect"],

        # -------------------------------------------------
        # SEO
        # -------------------------------------------------

        page_title=results["page_title"],
        meta_description=results["meta_description"],
        h1_count=results["h1_count"],

        # -------------------------------------------------
        # Advanced SEO
        # -------------------------------------------------

        h2_count=results["h2_count"],
        image_count=results["image_count"],
        missing_alt_count=results["missing_alt_count"],
        canonical_url=results["canonical_url"],
        has_viewport=results["has_viewport"],
        has_open_graph=results["has_open_graph"],
        has_twitter_card=results["has_twitter_card"],
        html_lang=results["html_lang"],
        has_favicon=results["has_favicon"],

        # -------------------------------------------------
        # Technology Detection
        # -------------------------------------------------

        cms=results["cms"],
        theme=results["theme"],
        technologies=results["technologies"],

        # -------------------------------------------------
        # Performance
        # -------------------------------------------------

        load_time=results["load_time"],
        performance_score=results["performance_score"],

        # -------------------------------------------------
        # Mobile
        # -------------------------------------------------

        mobile_friendly=results["mobile_friendly"],

        # -------------------------------------------------
        # Accessibility
        # -------------------------------------------------

        accessibility_score=results["accessibility_score"],

        # -------------------------------------------------
        # Scores
        # -------------------------------------------------

        seo_score=results["seo_score"],
        overall_score=results["overall_score"],

        # -------------------------------------------------
        # AI Recommendation Engine
        # -------------------------------------------------

        executive_summary=results["executive_summary"],
        critical_issues=results["critical_issues"],
        high_priority=results["high_priority"],
        medium_priority=results["medium_priority"],
        good_practices=results["good_practices"],

        # -------------------------------------------------
        # Business Opportunities
        # -------------------------------------------------

        opportunities=results["opportunities"],

        estimated_project_hours=results[
            "estimated_project_hours"
        ],

        estimated_project_value=results[
            "estimated_project_value"
        ],

        # -------------------------------------------------
        # Raw Results
        # -------------------------------------------------

        raw_results=results["raw_results"],
    )

    return redirect(
        "audits:detail",
        audit.pk,
    )