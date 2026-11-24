from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    # ==========================================================
    # Public Website (Landing Page)
    # ==========================================================
    path(
        "",
        include("apps.public.urls"),
    ),

    # ==========================================================
    # Dashboard
    # ==========================================================
    path(
        "dashboard/",
        include("apps.dashboard.urls"),
    ),

    # ==========================================================
    # Authentication
    # ==========================================================
    path(
        "accounts/",
        include("apps.accounts.urls"),
    ),

    # ==========================================================
    # Discovery
    # ==========================================================
    path(
        "discovery/",
        include("apps.discovery.urls"),
    ),

    # ==========================================================
    # Leads
    # ==========================================================
    path(
        "leads/",
        include("apps.leads.urls"),
    ),

    # ==========================================================
    # Website Audits
    # ==========================================================
    path(
        "audits/",
        include("apps.audits.urls"),
    ),

    # ==========================================================
    # Proposals
    # ==========================================================
    path(
        "proposals/",
        include("apps.proposals.urls"),
    ),

    # ==========================================================
    # Outreach
    # ==========================================================
    path(
        "outreach/",
        include("apps.outreach.urls"),
    ),

    # ==========================================================
    # Django Admin
    # ==========================================================
    path(
        "admin/",
        admin.site.urls,
    ),

    #path("api/", include("apps.api.urls")),

    path("pipeline/", include("apps.pipeline.urls")),

    path("calendar/", include("apps.crm_calendar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )