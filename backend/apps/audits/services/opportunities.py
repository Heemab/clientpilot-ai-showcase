"""
Business Opportunity Detection Engine
"""

from .pricing import estimate_service_price
from .effort import estimate_effort


def detect_opportunities(results):
    """
    Convert technical audit findings into
    business opportunities and estimate the
    implementation value.
    """

    opportunities = []

    # =====================================================
    # Website Speed Optimisation
    # =====================================================

    if results["load_time"] >= 3:

        opportunities.append({

            "service": "Website Speed Optimisation",

            "priority": "High",

            "estimated_hours": estimate_effort(
                "Website Speed Optimisation",
                results,
            ),

            "estimated_value": estimate_service_price(
                "Website Speed Optimisation",
                results,
            ),

            "reason": (
                f"Website loads in "
                f"{results['load_time']:.2f} seconds."
            ),

        })

    # =====================================================
    # SEO Optimisation
    # =====================================================

    if results["missing_alt_count"] > 0:

        opportunities.append({

            "service": "SEO Optimisation",

            "priority": "High",

            "estimated_hours": estimate_effort(
                "SEO Optimisation",
                results,
            ),

            "estimated_value": estimate_service_price(
                "SEO Optimisation",
                results,
            ),

            "reason": (
                f"{results['missing_alt_count']} "
                "images are missing ALT text."
            ),

        })

    # =====================================================
    # Technical SEO
    # =====================================================

    if not results["meta_description"]:

        opportunities.append({

            "service": "Technical SEO",

            "priority": "Medium",

            "estimated_hours": estimate_effort(
                "Technical SEO",
                results,
            ),

            "estimated_value": estimate_service_price(
                "Technical SEO",
                results,
            ),

            "reason": "Missing meta description.",

        })

    # =====================================================
    # On-page SEO
    # =====================================================

    if results["h1_count"] != 1:

        opportunities.append({

            "service": "On-page SEO",

            "priority": "Medium",

            "estimated_hours": estimate_effort(
                "On-page SEO",
                results,
            ),

            "estimated_value": estimate_service_price(
                "On-page SEO",
                results,
            ),

            "reason": "Heading structure needs improvement.",

        })

    # =====================================================
    # Security
    # =====================================================

    if not results["ssl_enabled"]:

        opportunities.append({

            "service": "SSL Installation",

            "priority": "Critical",

            "estimated_hours": estimate_effort(
                "SSL Installation",
                results,
            ),

            "estimated_value": estimate_service_price(
                "SSL Installation",
                results,
            ),

            "reason": "Website is not using HTTPS.",

        })

    if not results["https_redirect"]:

        opportunities.append({

            "service": "HTTPS Redirect Configuration",

            "priority": "High",

            "estimated_hours": estimate_effort(
                "HTTPS Redirect Configuration",
                results,
            ),

            "estimated_value": estimate_service_price(
                "HTTPS Redirect Configuration",
                results,
            ),

            "reason": "HTTP traffic is not redirected.",

        })

    # =====================================================
    # Accessibility
    # =====================================================

    if not results["html_lang"]:

        opportunities.append({

            "service": "Accessibility Compliance",

            "priority": "Medium",

            "estimated_hours": estimate_effort(
                "Accessibility Compliance",
                results,
            ),

            "estimated_value": estimate_service_price(
                "Accessibility Compliance",
                results,
            ),

            "reason": "HTML language attribute missing.",

        })

    # =====================================================
    # Social Media
    # =====================================================

    if not results["has_open_graph"]:

        opportunities.append({

            "service": "Social Media Optimisation",

            "priority": "Medium",

            "estimated_hours": estimate_effort(
                "Social Media Optimisation",
                results,
            ),

            "estimated_value": estimate_service_price(
                "Social Media Optimisation",
                results,
            ),

            "reason": "Open Graph metadata missing.",

        })

    if not results["has_twitter_card"]:

        opportunities.append({

            "service": "Twitter Card Optimisation",

            "priority": "Low",

            "estimated_hours": estimate_effort(
                "Twitter Card Optimisation",
                results,
            ),

            "estimated_value": estimate_service_price(
                "Twitter Card Optimisation",
                results,
            ),

            "reason": "Twitter Card metadata missing.",

        })

    # =====================================================
    # Website Care Plan
    # =====================================================

    opportunities.append({

        "service": "Website Care Plan",

        "priority": "Low",

        "estimated_hours": estimate_effort(
            "Website Care Plan",
            results,
        ),

        "estimated_value": estimate_service_price(
            "Website Care Plan",
            results,
        ),

        "reason": (
            "Ongoing maintenance, updates "
            "and monitoring recommended."
        ),

    })

    # =====================================================
    # Calculate Totals
    # =====================================================

    estimated_project_value = sum(
        opportunity["estimated_value"]
        for opportunity in opportunities
    )

    estimated_project_hours = sum(
        opportunity["estimated_hours"]
        for opportunity in opportunities
    )

    return {
        "opportunities": opportunities,
        "estimated_project_value": estimated_project_value,
        "estimated_project_hours": estimated_project_hours,
    }