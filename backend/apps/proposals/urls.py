from django.urls import path

from . import views

app_name = "proposals"

urlpatterns = [
    path(
        "",
        views.proposal_list,
        name="list",
    ),

    path(
        "generate/<int:audit_id>/",
        views.generate_proposal,
        name="generate_proposal",
    ),

    path(
        "<int:proposal_id>/",
        views.proposal_detail,
        name="proposal_detail",
    ),

    path(
        "<int:proposal_id>/pdf/",
        views.proposal_pdf,
        name="proposal_pdf",
    ),
]