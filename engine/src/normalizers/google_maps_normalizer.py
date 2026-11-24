from src.models.opportunity import Opportunity


class GoogleMapsNormalizer:
    """
    Converts Google Maps results into Opportunity objects.
    """

    def normalize(self, business):

        return Opportunity(

            source="Google Maps",

            business_name=business.get("title", ""),

            category=business.get("type", ""),

            address=business.get("address", ""),

            phone=business.get("phone", ""),

            website=business.get("website", ""),

            rating=float(business.get("rating", 0) or 0),

            reviews=int(business.get("reviews", 0) or 0),
        )