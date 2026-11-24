from .base import BaseProvider
from .google_provider import GoogleProvider
from .linkedin_provider import LinkedInProvider


class ProviderManager:
    """
    Manages all discovery providers.
    """

    def __init__(self):
        self._providers = {}

        # Register built-in providers
        self.register(GoogleProvider())
        self.register(LinkedInProvider())

    def register(self, provider: BaseProvider):
        """
        Register a provider.
        """
        self._providers[provider.provider_name] = provider

    def get(self, provider_name: str):
        """
        Return a registered provider.
        """
        return self._providers.get(provider_name)

    def all(self):
        """
        Return all registered providers.
        """
        return list(self._providers.values())