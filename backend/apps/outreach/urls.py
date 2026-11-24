from django.urls import path

from . import views

app_name = "outreach"

urlpatterns = [

    path(
        "",
        views.list_outreach,
        name="outreach_list",
    ),

    path(
        "generate/<int:proposal_id>/",
        views.generate,
        name="generate_outreach",
    ),

    path(
        "<int:outreach_id>/",
        views.detail,
        name="outreach_detail",
    ),

    path(
        "<int:outreach_id>/send/",
        views.send_email,
        name="send_email",
    ),

    path(
        "<int:outreach_id>/status/<str:status>/",
        views.update_status,
        name="outreach_status",
    ),

]