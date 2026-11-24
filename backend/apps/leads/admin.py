from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "status",
        "assigned_to",
        "organization",
        "created_at",
    )

    search_fields = (
        "company_name",
        "contact_name",
        "email",
    )

    list_filter = (
        "status",
        "organization",
    )

    ordering = ("-created_at",)