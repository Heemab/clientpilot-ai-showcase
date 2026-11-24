from typing import Any, Mapping

from apps.discovery.domain.discovery_result import DiscoveryResult


class GoogleMapsNormalizer:
    """
    Normalizes a raw Google Maps business record into the application's
    canonical DiscoveryResult value object.
    """

    def normalize(self, business: Mapping[str, Any]) -> DiscoveryResult:
        return DiscoveryResult(
            source="Google Maps",
            business_name=business.get("title", ""),
            category=business.get("type", ""),
            address=business.get("address", ""),
            phone=business.get("phone", ""),
            website=business.get("website", ""),
            rating=float(business.get("rating") or 0),
            reviews=int(business.get("reviews") or 0),
        )