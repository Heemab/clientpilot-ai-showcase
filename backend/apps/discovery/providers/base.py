from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Base class for all discovery providers.
    Every provider must implement the search() method.
    """

    provider_name = ""

    @abstractmethod
    def search(self, query: str, location: str = "") -> list:
        """
        Search for businesses/leads and return
        normalized lead dictionaries.
        """
        pass

    def is_available(self) -> bool:
        """
        Override if a provider needs API keys,
        authentication, etc.
        """
        return True