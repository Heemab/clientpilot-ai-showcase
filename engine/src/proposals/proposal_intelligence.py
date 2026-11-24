class ProposalIntelligence:
    """
    Converts technical findings into business-focused
    explanations suitable for client proposals.
    """

    def __init__(self):
        pass

    # --------------------------------------------------
    # Build Business Insights
    # --------------------------------------------------

    def build(self, findings):

        if not findings:

            return [

                {
                    "title": "Website Review",
                    "impact": (
                        "A detailed technical review was completed. "
                        "Additional opportunities can be identified "
                        "during a live consultation."
                    ),
                    "recommendation": (
                        "Carry out a full website audit to uncover "
                        "additional opportunities for growth."
                    ),
                    "priority": "Medium",
                }

            ]

        insights = []

        for finding in findings:

            lower = finding.lower()

            # --------------------------------------------------
            # SSL
            # --------------------------------------------------

            if "ssl" in lower or "https" in lower:

                insights.append({

                    "title":
                        "Website Security",

                    "impact":
                        (
                            "Visitors are more likely to trust and "
                            "contact businesses whose websites are "
                            "secure. A missing SSL certificate may "
                            "reduce enquiry rates."
                        ),

                    "recommendation":
                        (
                            "Install and correctly configure SSL "
                            "across the website."
                        ),

                    "priority":
                        "High",

                })

            # --------------------------------------------------
            # Contact Form
            # --------------------------------------------------

            elif "contact form" in lower:

                insights.append({

                    "title":
                        "Lead Generation",

                    "impact":
                        (
                            "Potential customers may leave the "
                            "website without making contact if there "
                            "is no simple enquiry process."
                        ),

                    "recommendation":
                        (
                            "Implement a clear enquiry form on key "
                            "pages."
                        ),

                    "priority":
                        "High",

                })

            # --------------------------------------------------
            # Email
            # --------------------------------------------------

            elif "email" in lower:

                insights.append({

                    "title":
                        "Professional Branding",

                    "impact":
                        (
                            "A professional business email increases "
                            "credibility and customer confidence."
                        ),

                    "recommendation":
                        (
                            "Create a branded business email address."
                        ),

                    "priority":
                        "Medium",

                })

            # --------------------------------------------------
            # SEO
            # --------------------------------------------------

            elif "meta" in lower or "title" in lower:

                insights.append({

                    "title":
                        "Search Visibility",

                    "impact":
                        (
                            "Search engines rely on page titles and "
                            "descriptions to understand your website. "
                            "Missing metadata may reduce visibility."
                        ),

                    "recommendation":
                        (
                            "Optimise page titles and meta "
                            "descriptions."
                        ),

                    "priority":
                        "Medium",

                })

            # --------------------------------------------------
            # Default
            # --------------------------------------------------

            else:

                insights.append({

                    "title":
                        "Website Improvement",

                    "impact":
                        finding,

                    "recommendation":
                        (
                            "Review and implement the recommended "
                            "improvements."
                        ),

                    "priority":
                        "Medium",

                })

        return insights