from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render

from apps.discovery.domain.discovery_result import DiscoveryResult
from apps.discovery.services.discovery_service import DiscoveryService
from apps.discovery.services.lead_import_service import LeadImportService


@login_required
def index(request):
    """
    Discovery dashboard.
    Search businesses from discovery providers.
    """

    query = request.POST.get("query", "").strip()
    location = request.POST.get("location", "United States").strip()

    discovery_service = DiscoveryService()

    businesses = []
    is_synthetic = False

    if query:
        businesses = discovery_service.search(query, location)

        # Demo fallback
        if not businesses:
            is_synthetic = True
            businesses = [
                DiscoveryResult(
                    source="Synthetic demo",
                    business_name="Bright Dental Clinic",
                    category="Dentist",
                    address="Chicago, IL",
                    phone="(312) 555-0147",
                    website="https://brightdental.example",
                    rating=4.8,
                    reviews=214,
                ),
                DiscoveryResult(
                    source="Synthetic demo",
                    business_name="NorthStar Accounting",
                    category="Accountant",
                    address="New York, NY",
                    phone="(212) 555-0198",
                    website="https://northstar.example",
                    rating=4.9,
                    reviews=163,
                ),
                DiscoveryResult(
                    source="Synthetic demo",
                    business_name="Elite Roofing Ltd",
                    category="Roofing Contractor",
                    address="Dallas, TX",
                    phone="(972) 555-0102",
                    website="https://eliteroofing.example",
                    rating=4.7,
                    reviews=98,
                ),
            ]

    if request.method == "POST":
        request.session["discovery_results"] = [business.to_dict() for business in businesses]

    return render(
        request,
        "discovery/index.html",
        {
            "businesses": businesses,
            "is_synthetic": is_synthetic,
            "query": query,
            "location": location,
        },
    )


@login_required
def import_lead(request):
    """
    Import a single discovered business.
    """

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    organization = request.user.organization

    if organization is None:
        messages.error(
            request,
            "Your account is not assigned to an organization.",
        )
        return redirect("discovery:index")

    result = DiscoveryResult(
        source="Google Maps",
        business_name=request.POST.get("company_name", "").strip(),
        category=request.POST.get("category", "").strip(),
        address=request.POST.get("address", "").strip(),
        phone=request.POST.get("phone", "").strip(),
        website=request.POST.get("website", "").strip(),
        rating=float(request.POST.get("rating") or 0),
        reviews=int(request.POST.get("reviews") or 0),
    )

    lead, created = LeadImportService().import_result(
        organization=organization,
        result=result,
    )

    if lead is None:
        messages.error(
            request,
            "This business cannot be imported because no website was found.",
        )
    elif created:
        messages.success(
            request,
            f"{lead.company_name} imported successfully.",
        )
    else:
        messages.info(
            request,
            f"{lead.company_name} already exists in your CRM.",
        )

    return redirect("discovery:index")


@login_required
def import_all(request):
    """
    Import all businesses from the latest discovery search.
    """

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    organization = request.user.organization

    if organization is None:
        messages.error(
            request,
            "Your account is not assigned to an organization.",
        )
        return redirect("discovery:index")

    stored_results = request.session.get(
        "discovery_results",
        [],
    )

    if not stored_results:
        messages.warning(
            request,
            "No discovery results available. Please run a search first.",
        )
        return redirect("discovery:index")

    results = [
        DiscoveryResult.from_dict(item)
        for item in stored_results
    ]

    summary = LeadImportService().import_results(
        organization=organization,
        results=results,
    )

    messages.success(
        request,
        (
            f"Import completed. "
            f"✅ {summary.imported} imported • "
            f"⚠️ {summary.duplicates} already existed • "
            f"⏭️ {summary.skipped} skipped (no website)"
        ),
    )

    return redirect("discovery:index")