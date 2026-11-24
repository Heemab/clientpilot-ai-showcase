from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [

    # ==========================
    # Lead CRUD
    # ==========================

    path(
        "",
        views.lead_list,
        name="list",
    ),

    path(
        "create/",
        views.lead_create,
        name="create",
    ),

    path(
        "<int:pk>/",
        views.lead_detail,
        name="lead_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.lead_edit,
        name="lead_edit",
    ),

    path(
        "<int:pk>/delete/",
        views.lead_delete,
        name="lead_delete",
    ),

    path(
        "<int:pk>/pipeline/",
        views.run_pipeline,
        name="pipeline",
    ),

    # ==========================
    # CRM Tasks
    # ==========================

    path(
        "<int:pk>/tasks/create/",
        views.task_create,
        name="task_create",
    ),

    path(
        "tasks/<int:task_id>/edit/",
        views.task_edit,
        name="task_edit",
    ),

    path(
        "tasks/<int:task_id>/complete/",
        views.task_complete,
        name="task_complete",
    ),

    path(
        "tasks/<int:task_id>/delete/",
        views.task_delete,
        name="task_delete",
    ),
]