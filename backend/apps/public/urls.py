from django.urls import path

from . import views

app_name = "public"

urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "demo/",
        views.demo,
        name="demo",
    ),

    path(
        "contact/",
        views.contact,
        name="contact",
    ),
]