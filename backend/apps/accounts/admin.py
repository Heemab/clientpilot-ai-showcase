from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "organization",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "organization",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Organization Information",
            {
                "fields": (
                    "organization",
                    "phone",
                    "job_title",
                    "avatar",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Organization Information",
            {
                "fields": (
                    "organization",
                    "phone",
                    "job_title",
                    "avatar",
                )
            },
        ),
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )

    ordering = ("username",)