from serpapi import GoogleSearch

from cae_config.settings import Settings


class GoogleMapsService:
    """
    Handles Google Maps searches using SerpAPI.
    """

    def search(self, query, location="Lagos, Nigeria"):

        params = {
            "engine": "google_maps",
            "q": query,
            "location": location,
            "z": 13,          # Required with location
            "type": "search",
            "api_key": Settings.SERPAPI_API_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()


        return results.get("local_results", [])