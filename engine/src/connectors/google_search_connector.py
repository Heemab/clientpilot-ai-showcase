from src.connectors.base_connector import BaseConnector


class GoogleSearchConnector(BaseConnector):

    def __init__(self):
        super().__init__("Google Search")

    def search(self):
        print("Searching Google...")

    def collect(self):
        print("Collecting search results...")

    def save(self):
        print("Saving results...")