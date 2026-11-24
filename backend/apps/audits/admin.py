from django.contrib import admin

from .models import Audit


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):

    list_display = (
        "lead",
        "overall_score",
        "seo_score",
        "performance_score",
        "ssl_enabled",
        "mobile_friendly",
        "created_at",
    )

    list_filter = (
        "ssl_enabled",
        "mobile_friendly",
        "created_at",
    )

    search_fields = (
        "lead__company_name",
        "website",
    )

    ordering = (
        "-created_at",
    )