from django.urls import path

from .views import (
    BestOpportunityView,
    DashboardView,
    EngineHealthView,
    ProposalView,
)

urlpatterns = [
    path("engine/health/", EngineHealthView.as_view(), name="engine-health"),
    path("engine/dashboard/", DashboardView.as_view(), name="engine-dashboard"),
    path(
        "engine/opportunity/best/",
        BestOpportunityView.as_view(),
        name="engine-best-opportunity",
    ),
    path(
        "engine/proposal/",
        ProposalView.as_view(),
        name="engine-proposal",
    ),
]