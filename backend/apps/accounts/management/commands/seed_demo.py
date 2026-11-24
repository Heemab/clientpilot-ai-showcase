from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.leads.models import Lead, LeadTask


class Command(BaseCommand):
    help = "Add synthetic CRM records to an existing local user's organization."

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)

    @transaction.atomic
    def handle(self, *args, **options):
        user = get_user_model().objects.filter(username=options["username"]).first()
        if not user or not user.organization_id:
            raise CommandError("Register a local account with an organization first.")

        lead, _ = Lead.objects.get_or_create(
            organization=user.organization,
            company_name="Sample Orchard Studio",
            email="orchard@example.invalid",
            defaults={
                "website": "https://orchard.example.invalid",
                "category": "Design studio",
                "notes": "Fictional business for the local demo.",
                "status": "qualified",
                "source": "Synthetic demo",
            },
        )
        LeadTask.objects.get_or_create(
            lead=lead,
            title="Review the sample prospect",
            defaults={"description": "Prepare questions for a fictional discovery call."},
        )
        self.stdout.write(self.style.SUCCESS("Synthetic lead and task are ready."))
