class PricingEngine:
    """
    Estimates the value, effort and ROI of a project.

    This class contains pricing logic only.
    BusinessIntelligence should call this class instead
    of hard-coding project values.
    """

    def __init__(self):

        self.base_prices = {

            "Website Audit": 500,

            "Website Redesign": 2500,

            "WordPress Maintenance": 750,

            "Website Security": 600,

            "Speed Optimization": 700,

            "Local SEO": 1200,

            "Performance Optimization": 900,

            "Technical SEO": 1000,

            "Shopify Optimization": 1400,

            "Conversion Optimization": 1200,

            "Drupal Maintenance": 1500,

            "Security Updates": 900,

            "Professional Email Setup": 350,

            "SSL Installation": 250,

            "SEO Meta Optimization": 500,

            "SEO Title Optimization": 400,

            "Contact Form Improvement": 450,

        }

    # --------------------------------------------------

    def estimate(
        self,
        primary_service,
        technology,
        reviews,
        website_quality,
        services_count,
    ):
        """
        Estimate the project based on multiple factors.
        """

        value = self.base_prices.get(
            primary_service,
            750
        )

        # ------------------------------------------
        # Technology Complexity
        # ------------------------------------------

        if technology in (
            "Unknown",
            "Custom / Unknown",
        ):

            value += 800

        elif technology in (
            "React",
            "Next.js",
        ):

            value += 600

        elif technology == "Drupal":

            value += 900

        elif technology == "Shopify":

            value += 500

        elif technology == "WordPress":

            value += 250

        # ------------------------------------------
        # Website Quality
        # ------------------------------------------

        if website_quality < 40:

            value += 1500

        elif website_quality < 60:

            value += 1000

        elif website_quality < 80:

            value += 500

        # ------------------------------------------
        # Business Size
        # ------------------------------------------

        if reviews > 5000:

            value += 2500

        elif reviews > 2000:

            value += 1800

        elif reviews > 1000:

            value += 1200

        elif reviews > 500:

            value += 800

        elif reviews > 100:

            value += 400

        # ------------------------------------------
        # Multiple Opportunities
        # ------------------------------------------

        value += services_count * 150

        # ------------------------------------------
        # Estimated Hours
        # ------------------------------------------

        hours = max(
            4,
            round(value / 250)
        )

        # ------------------------------------------
        # Difficulty
        # ------------------------------------------

        if value >= 5000:

            difficulty = "Hard"

        elif value >= 2500:

            difficulty = "Medium"

        else:

            difficulty = "Easy"

        return {

            "estimated_value": round(value),

            "estimated_hours": hours,

            "difficulty": difficulty,

        }