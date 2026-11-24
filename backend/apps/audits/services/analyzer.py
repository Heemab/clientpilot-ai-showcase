from .utils import fetch_page, normalize_url
from .ssl import analyze_ssl
from .seo import analyze_seo
from .technology import detect_technology
from .recommendations import generate_recommendations
from .scoring import calculate_scores
from .opportunities import detect_opportunities


class WebsiteAuditService:
    """
    Main website audit orchestrator.
    """

    @classmethod
    def run(cls, website):

        website = normalize_url(website)

        results = {

            # -------------------------------------------------
            # Website
            # -------------------------------------------------

            "website": website,

            # -------------------------------------------------
            # Security
            # -------------------------------------------------

            "ssl_enabled": False,
            "https_redirect": False,

            # -------------------------------------------------
            # SEO
            # -------------------------------------------------

            "page_title": "",
            "meta_description": "",
            "h1_count": 0,

            # -------------------------------------------------
            # Advanced SEO
            # -------------------------------------------------

            "h2_count": 0,
            "image_count": 0,
            "missing_alt_count": 0,
            "canonical_url": "",
            "has_viewport": False,
            "has_open_graph": False,
            "has_twitter_card": False,
            "html_lang": "",
            "has_favicon": False,

            # -------------------------------------------------
            # Technology Detection
            # -------------------------------------------------

            "cms": "Unknown",
            "theme": "Unknown",
            "technologies": [],

            # -------------------------------------------------
            # Performance
            # -------------------------------------------------

            "load_time": 0,
            "performance_score": 0,

            # -------------------------------------------------
            # Mobile
            # -------------------------------------------------

            "mobile_friendly": False,

            # -------------------------------------------------
            # Accessibility
            # -------------------------------------------------

            "accessibility_score": 0,

            # -------------------------------------------------
            # Scores
            # -------------------------------------------------

            "seo_score": 0,
            "overall_score": 0,

            # -------------------------------------------------
            # AI Recommendation Engine
            # -------------------------------------------------

            "executive_summary": "",
            "critical_issues": [],
            "high_priority": [],
            "medium_priority": [],
            "good_practices": [],

            # -------------------------------------------------
            # Business Opportunities
            # -------------------------------------------------

            "opportunities": [],
            "estimated_project_hours": 0,
            "estimated_project_value": 0,

            # -------------------------------------------------
            # Raw Results
            # -------------------------------------------------

            "raw_results": {},
        }

        try:

            response, soup, elapsed = fetch_page(website)

            results["load_time"] = elapsed

            # -------------------------------------------------
            # Security
            # -------------------------------------------------

            results.update(
                analyze_ssl(
                    website,
                    response,
                )
            )

            # -------------------------------------------------
            # SEO
            # -------------------------------------------------

            results.update(
                analyze_seo(
                    soup,
                )
            )

            # -------------------------------------------------
            # Technology Detection
            # -------------------------------------------------

            results.update(
                detect_technology(
                    response,
                    soup,
                )
            )

            # -------------------------------------------------
            # Calculate Scores
            # -------------------------------------------------

            results = calculate_scores(results)

            # -------------------------------------------------
            # AI Recommendations
            # -------------------------------------------------

            results.update(
                generate_recommendations(results)
            )

            # -------------------------------------------------
            # Business Opportunities
            # -------------------------------------------------

            opportunity_data = detect_opportunities(results)

            results["opportunities"] = opportunity_data[
                "opportunities"
            ]

            results["estimated_project_hours"] = opportunity_data[
                "estimated_project_hours"
            ]

            results["estimated_project_value"] = opportunity_data[
                "estimated_project_value"
            ]

            # -------------------------------------------------
            # Raw Response
            # -------------------------------------------------

            results["raw_results"] = {
                "status_code": response.status_code,
                "final_url": response.url,
                "headers": dict(response.headers),
            }

        except Exception as exc:

            results["executive_summary"] = "Audit failed."

            results["critical_issues"] = [
                str(exc)
            ]

            results["high_priority"] = []

            results["medium_priority"] = []

            results["good_practices"] = []

            results["opportunities"] = []

            results["estimated_project_hours"] = 0

            results["estimated_project_value"] = 0

        return results