from .base import BaseProvider

from apps.discovery.services.linkedin_service import LinkedInService
from apps.discovery.services.linkedin_normalizer import LinkedInNormalizer


class LinkedInProvider(BaseProvider):

    provider_name = "linkedin"

    def __init__(self):
        self.service = LinkedInService()
        self.normalizer = LinkedInNormalizer()

    def search(self, query: str, location: str = "") -> list:
        leads = self.service.search(query, location)

        return [
            self.normalizer.normalize(item)
            for item in leads
        ]