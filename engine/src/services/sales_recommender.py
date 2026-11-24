class SalesRecommender:
    """
    Converts recommended services into
    a sales strategy.
    """

    def __init__(self):

        self.pricing = {

            "Website Audit": ("$200 - $500", "Easy"),

            "Website Redesign": ("$800 - $2,500", "Medium"),

            "Website Development": ("$2,000 - $5,000", "Hard"),

            "WordPress Maintenance": ("$150 - $400", "Easy"),

            "Website Security": ("$250 - $600", "Easy"),

            "Speed Optimization": ("$200 - $600", "Medium"),

            "Local SEO": ("$300 - $900", "Medium"),

            "Technical SEO": ("$400 - $1,000", "Medium"),

            "Performance Optimization": ("$300 - $800", "Medium"),

            "Shopify Optimization": ("$300 - $900", "Medium"),

            "Conversion Optimization": ("$500 - $1,500", "Hard"),

            "Professional Email Setup": ("$100 - $250", "Easy"),

            "SSL Installation": ("$80 - $200", "Easy"),

            "SEO Meta Optimization": ("$150 - $350", "Easy"),

            "SEO Title Optimization": ("$150 - $350", "Easy"),

            "Contact Form Improvement": ("$100 - $300", "Easy"),
        }

    def recommend(self, opportunity):

        if not opportunity.recommended_services:

            return {}

        services = [

            s.strip()

            for s in opportunity.recommended_services.split(",")

        ]

        primary = services[0]

        value, difficulty = self.pricing.get(

            primary,

            ("Custom Quote", "Unknown")

        )

        pitch = (

            f"I noticed your business could benefit from "

            f"{primary.lower()}. "

            f"This is a service I regularly provide and "

            f"I'd be happy to offer a free assessment "

            f"and discuss the best solution for your business."

        )

        return {

    "primary_service": primary,

    "estimated_value": value,

    "difficulty": difficulty,

    "reason": f"Recommended because '{primary}' is the highest priority service identified during website analysis."
}