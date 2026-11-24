from serpapi import GoogleSearch

from django.conf import settings


class GoogleMapsService:
    """
    Handles Google Maps searches using SerpAPI.
    """

    def search(self, query, location="Lagos, Nigeria"):

        if not settings.SERPAPI_API_KEY:
            return []

        params = {
            "engine": "google_maps",
            "q": query,
            "location": location,
            "z": 13,
            "type": "search",
            "api_key": settings.SERPAPI_API_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()


        return results.get("local_results", [])