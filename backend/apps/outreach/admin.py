from django.contrib import admin

from .models import Outreach


@admin.register(Outreach)
class OutreachAdmin(admin.ModelAdmin):

    list_display = (
        "proposal",
        "subject",
        "created_at",
    )

    search_fields = (
        "proposal__proposal_number",
        "proposal__lead__company_name",
        "subject",
    )

    list_filter = (
        "created_at",
    )