from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "website",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = ("name",)