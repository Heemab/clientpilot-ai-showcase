from .base import BaseProvider

from apps.discovery.services.google_maps_service import GoogleMapsService
from apps.discovery.services.google_maps_normalizer import GoogleMapsNormalizer


class GoogleProvider(BaseProvider):
    """
    Google Maps discovery provider.
    Wraps the existing service and normalizer.
    """

    provider_name = "google_maps"

    def __init__(self):
        self.service = GoogleMapsService()
        self.normalizer = GoogleMapsNormalizer()

    def search(self, query: str, location: str = "") -> list:
        businesses = self.service.search(query, location)

        return [
            self.normalizer.normalize(business)
            for business in businesses
        ]