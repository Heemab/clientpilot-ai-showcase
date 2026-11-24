from dataclasses import dataclass
from typing import Iterable

from apps.discovery.domain.discovery_result import DiscoveryResult
from apps.leads.models import Lead


@dataclass(slots=True)
class ImportSummary:
    """
    Summary of a bulk lead import operation.
    """

    imported: int = 0
    duplicates: int = 0
    skipped: int = 0


class LeadImportService:
    """
    Imports DiscoveryResult objects into the CRM.

    This service is the ONLY component responsible for creating
    Lead records from discovery providers.

    Supported providers:
    - Google Maps
    - LinkedIn
    - Freelancer
    - Guru
    - PeoplePerHour
    - Apollo
    - CSV imports
    """

    DEFAULT_STATUS = "new"
    DEFAULT_PRIORITY = "medium"

    def import_result(
        self,
        *,
        organization,
        result: DiscoveryResult,
    ) -> tuple[Lead | None, bool]:
        """
        Import a single DiscoveryResult.

        Returns:
            (lead, created)

            created=True  -> New lead created
            created=False -> Lead already existed
        """

        website = result.website.strip()

        if not website:
            return None, False

        lead, created = Lead.objects.get_or_create(
            organization=organization,
            website=website,
            defaults=self._build_defaults(result),
        )

        return lead, created

    def import_results(
        self,
        *,
        organization,
        results: Iterable[DiscoveryResult],
    ) -> ImportSummary:
        """
        Import multiple DiscoveryResult objects.
        """

        summary = ImportSummary()

        for result in results:

            if not result.website.strip():
                summary.skipped += 1
                continue

            _, created = self.import_result(
                organization=organization,
                result=result,
            )

            if created:
                summary.imported += 1
            else:
                summary.duplicates += 1

        return summary

    def lead_exists(
        self,
        *,
        organization,
        website: str,
    ) -> bool:
        """
        Check whether a lead already exists.
        """

        website = website.strip()

        if not website:
            return False

        return Lead.objects.filter(
            organization=organization,
            website=website,
        ).exists()

    def _build_defaults(
        self,
        result: DiscoveryResult,
    ) -> dict:
        """
        Build Lead defaults from a DiscoveryResult.
        """

        return {
            "company_name": result.business_name,
            "contact_name": "",
            "email": "",
            "phone": result.phone,
            "website": result.website,
            "address": result.address,
            "category": result.category,
            "source": result.source,
            "rating": result.rating,
            "reviews": result.reviews,
            "status": self.DEFAULT_STATUS,
            "priority": self.DEFAULT_PRIORITY,
            "notes": f"Imported from {result.source}",
        }