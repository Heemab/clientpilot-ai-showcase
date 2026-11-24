from django.urls import path

from . import views

app_name = "audits"

urlpatterns = [
    path(
        "",
        views.audit_list,
        name="list",
    ),
    path(
        "<int:pk>/",
        views.audit_detail,
        name="detail",
    ),
    path(
        "lead/<int:lead_id>/run/",
        views.run_audit,
        name="run",
    ),
]