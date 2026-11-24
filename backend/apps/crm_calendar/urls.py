from django.urls import path

from . import views

app_name = "crm_calendar"

urlpatterns = [
    path("", views.index, name="index"),
]