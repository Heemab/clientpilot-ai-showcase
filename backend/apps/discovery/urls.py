from django.urls import path

from . import views

app_name = "discovery"

urlpatterns = [
    path("", views.index, name="index"),

    path(
        "import/",
        views.import_lead,
        name="import",
    ),

    path(
        "import-all/",
        views.import_all,
        name="import_all",
    ),
]