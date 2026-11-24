from abc import ABC, abstractmethod


class BaseConnector(ABC):
    """
    Base class for every connector.
    """

    def __init__(self, source_name):
        self.source_name = source_name

    @abstractmethod
    def search(self):
        """Search for opportunities."""
        pass

    @abstractmethod
    def collect(self):
        """Collect opportunity data."""
        pass

    @abstractmethod
    def save(self):
        """Save data into the database."""
        pass

    def info(self):
        print(f"Connector Loaded: {self.source_name}")