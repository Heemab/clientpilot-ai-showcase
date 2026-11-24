from apps.discovery.providers.manager import ProviderManager


class DiscoveryService:

    def __init__(self):
        self.providers = ProviderManager()

    def search(self, query, location, providers=None):
        if providers is None:
            providers = ["google_maps"]

        results = []

        for provider_name in providers:
            provider = self.providers.get(provider_name)

            if provider:
                results.extend(
                    provider.search(query, location)
                )

        return results