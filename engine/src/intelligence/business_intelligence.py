from src.intelligence.pricing_engine import PricingEngine


class BusinessIntelligence:
    """
    Central intelligence engine.

    Converts website analysis into business,
    sales and CRM intelligence.

    Every future module should consume this class.
    """

    def __init__(self):

        self.pricing = PricingEngine()

    # --------------------------------------------------
    # Analyze Business
    # --------------------------------------------------

    def analyze(self, opportunity, report):

        technology = report.get(
            "technology",
            "Unknown"
        )

        intelligence = {

            "technology": technology,

            "website_quality": 100,

            "priority": "LOW",

            "recommended_services": [],

            "primary_service": "",

            "estimated_value": 0,

            "estimated_hours": 0,

            "difficulty": "Easy",

            "closing_probability": 0,

            "roi_score": 0,

            "sales_notes": [],

            "reason": "",

        }

        # --------------------------------------------------
        # Website Quality
        # --------------------------------------------------

        if not report.get("website_exists", False):
            intelligence["website_quality"] -= 60

        if not report.get("https", False):
            intelligence["website_quality"] -= 15

        if not report.get("contact_form", False):
            intelligence["website_quality"] -= 10

        if not report.get("email_found", False):
            intelligence["website_quality"] -= 5

        if not report.get("meta_description", False):
            intelligence["website_quality"] -= 5

        if not report.get("title", False):
            intelligence["website_quality"] -= 5

        intelligence["website_quality"] = max(
            0,
            intelligence["website_quality"]
        )

        # --------------------------------------------------
        # Technology Recommendations
        # --------------------------------------------------

        if technology == "WordPress":

            intelligence["recommended_services"].extend([
                "WordPress Maintenance",
                "Website Security",
                "Speed Optimization",
            ])

        elif technology == "Shopify":

            intelligence["recommended_services"].extend([
                "Shopify Optimization",
                "Conversion Optimization",
            ])

        elif technology == "Wix":

            intelligence["recommended_services"].extend([
                "Website Redesign",
                "Local SEO",
            ])

        elif technology == "Next.js":

            intelligence["recommended_services"].extend([
                "Performance Optimization",
                "Technical SEO",
            ])

        elif technology == "React":

            intelligence["recommended_services"].extend([
                "Performance Optimization",
                "Technical SEO",
            ])

        elif technology == "Squarespace":

            intelligence["recommended_services"].extend([
                "Website Redesign",
                "Local SEO",
            ])

        elif technology == "Drupal":

            intelligence["recommended_services"].extend([
                "Drupal Maintenance",
                "Security Updates",
            ])

        else:

            intelligence["recommended_services"].append(
                "Website Audit"
            )

        # --------------------------------------------------
        # Website Issues
        # --------------------------------------------------

        if opportunity.reviews < 100:
            intelligence["recommended_services"].append(
                "Local SEO"
            )

        if not report.get("email_found", False):
            intelligence["recommended_services"].append(
                "Professional Email Setup"
            )

        if not report.get("contact_form", False):
            intelligence["recommended_services"].append(
                "Contact Form Improvement"
            )

        if not report.get("https", False):
            intelligence["recommended_services"].append(
                "SSL Installation"
            )

        if not report.get("meta_description", False):
            intelligence["recommended_services"].append(
                "SEO Meta Optimization"
            )

        if not report.get("title", False):
            intelligence["recommended_services"].append(
                "SEO Title Optimization"
            )

        # --------------------------------------------------
        # Remove Duplicates
        # --------------------------------------------------

        intelligence["recommended_services"] = list(
            dict.fromkeys(
                intelligence["recommended_services"]
            )
        )

        # --------------------------------------------------
        # Primary Service
        # --------------------------------------------------

        if intelligence["recommended_services"]:

            intelligence["primary_service"] = (
                intelligence["recommended_services"][0]
            )

        else:

            intelligence["primary_service"] = "Website Audit"

        # --------------------------------------------------
        # Pricing Engine
        # --------------------------------------------------

        pricing = self.pricing.estimate(

            primary_service=intelligence["primary_service"],

            technology=technology,

            reviews=opportunity.reviews,

            website_quality=intelligence["website_quality"],

            services_count=len(
                intelligence["recommended_services"]
            ),
        )

        intelligence["estimated_value"] = pricing[
            "estimated_value"
        ]

        intelligence["estimated_hours"] = pricing[
            "estimated_hours"
        ]

        intelligence["difficulty"] = pricing[
            "difficulty"
        ]

        # --------------------------------------------------
        # Priority
        # --------------------------------------------------

        score = opportunity.opportunity_score

        if score >= 70:

            intelligence["priority"] = "HIGH"

            intelligence["closing_probability"] = 90

        elif score >= 40:

            intelligence["priority"] = "MEDIUM"

            intelligence["closing_probability"] = 75

        else:

            intelligence["priority"] = "LOW"

            intelligence["closing_probability"] = 60

        # --------------------------------------------------
        # ROI Score
        # --------------------------------------------------

        hours = max(
            intelligence["estimated_hours"],
            1
        )

        intelligence["roi_score"] = round(

            (
                intelligence["estimated_value"]
                * intelligence["closing_probability"]
                / 100
            )

            / hours

        )

        # --------------------------------------------------
        # Sales Notes
        # --------------------------------------------------

        intelligence["sales_notes"] = [

            f"Technology: {technology}",

            f"Google Rating: {opportunity.rating}",

            f"Google Reviews: {opportunity.reviews}",

            f"Website Quality: {intelligence['website_quality']}",

            f"Primary Service: {intelligence['primary_service']}",

            f"Estimated Value: ${intelligence['estimated_value']:,}",

        ]

        # --------------------------------------------------
        # Sales Reason
        # --------------------------------------------------

        intelligence["reason"] = (
            f"{technology} website with "
            f"{opportunity.reviews} Google reviews, "
            f"website quality score of "
            f"{intelligence['website_quality']} "
            f"and primary recommendation of "
            f"{intelligence['primary_service']}."
        )

        return intelligence