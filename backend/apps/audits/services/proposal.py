"""
Proposal Builder

Converts audit results into a structured
proposal object that can be rendered as
HTML, PDF, email or CRM opportunity.
"""

from datetime import timedelta


def estimate_timeline(opportunities):
    """
    Estimate delivery time based on effort.
    """

    total_hours = sum(
        item.get("estimated_hours", 0)
        for item in opportunities
    )

    days = max(1, round(total_hours / 6))

    return f"{days}-{days + 2} business days"


def build_proposal(lead, audit):
    """
    Build a proposal dictionary.
    """

    total_hours = sum(
        item.get("estimated_hours", 0)
        for item in audit.opportunities
    )

    proposal = {

        "client": {

            "company": lead.company_name,

            "website": lead.website,

        },

        "audit": {

            "score": audit.overall_score,

            "seo_score": audit.seo_score,

            "performance_score": audit.performance_score,

            "accessibility_score": audit.accessibility_score,

        },

        "summary": audit.executive_summary,

        "services": audit.opportunities,

        "estimated_hours": total_hours,

        "estimated_value": audit.estimated_project_value,

        "timeline": estimate_timeline(
            audit.opportunities
        ),

        "deliverables": [

            "Website optimisation",

            "SEO improvements",

            "Performance optimisation",

            "Accessibility improvements",

            "Testing and quality assurance",

        ],

        "next_steps": [

            "Approve proposal",

            "Schedule kickoff meeting",

            "Begin implementation",

        ],

    }

    return proposal