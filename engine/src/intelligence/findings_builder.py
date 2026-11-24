class FindingsBuilder:
    """
    Converts technical website analysis into:

    1. Human-readable findings (legacy)
    2. Structured findings for proposals
    """

    # --------------------------------------------------
    # Legacy Findings
    # --------------------------------------------------

    def build(self, report):

        findings = []

        if not report.get("website_exists", False):

            findings.append(
                "No working website was detected."
            )

            return findings

        if not report.get("https", False):

            findings.append(
                "The website does not appear to use SSL (HTTPS), which can reduce visitor trust."
            )

        if not report.get("contact_form", False):

            findings.append(
                "A contact form could not be found, which may make it harder for potential customers to get in touch."
            )

        if not report.get("email_found", False):

            findings.append(
                "No professional business email address was detected."
            )

        if not report.get("title"):

            findings.append(
                "The homepage appears to be missing an optimized page title."
            )

        if not report.get("meta_description"):

            findings.append(
                "The homepage appears to be missing a meta description, which can reduce search visibility."
            )

        technology = report.get(
            "technology",
            "Unknown"
        )

        if technology in (
            "Unknown",
            "Custom / Unknown",
        ):

            findings.append(
                "The website appears to use a custom or unidentified platform, which may benefit from a technical review."
            )

        elif technology == "WordPress":

            findings.append(
                "The website is built with WordPress, which offers many opportunities for performance and SEO improvements."
            )

        elif technology == "Shopify":

            findings.append(
                "The website uses Shopify, providing opportunities for conversion and store optimization."
            )

        elif technology == "Wix":

            findings.append(
                "The website is built with Wix, which may benefit from improvements to performance and local SEO."
            )

        return findings

    # --------------------------------------------------
    # Structured Findings
    # --------------------------------------------------

    def build_structured(self, report):

        findings = []

        if not report.get("website_exists", False):

            findings.append({

                "title":
                    "Website Availability",

                "priority":
                    "Critical",

                "evidence":
                    "No working website could be reached.",

                "impact":
                    (
                        "Potential customers may be unable "
                        "to learn about your business online."
                    ),

                "recommendation":
                    (
                        "Launch a professional business "
                        "website as a priority."
                    ),

            })

            return findings

        # ----------------------------------------------

        if not report.get("https", False):

            findings.append({

                "title":
                    "Website Security",

                "priority":
                    "High",

                "evidence":
                    "HTTPS / SSL was not detected.",

                "impact":
                    (
                        "Modern browsers may warn visitors "
                        "that the website is not secure, "
                        "reducing customer trust."
                    ),

                "recommendation":
                    "Install an SSL certificate."

            })

        # ----------------------------------------------

        if not report.get("contact_form", False):

            findings.append({

                "title":
                    "Lead Generation",

                "priority":
                    "High",

                "evidence":
                    "No contact form was detected.",

                "impact":
                    (
                        "Visitors have fewer ways to make "
                        "enquiries, reducing conversion."
                    ),

                "recommendation":
                    "Add a simple enquiry form."

            })

        # ----------------------------------------------

        if not report.get("email_found", False):

            findings.append({

                "title":
                    "Professional Branding",

                "priority":
                    "Medium",

                "evidence":
                    "No professional email address detected.",

                "impact":
                    (
                        "A branded email improves "
                        "credibility and trust."
                    ),

                "recommendation":
                    "Create a branded business email."

            })

        # ----------------------------------------------

        if not report.get("title"):

            findings.append({

                "title":
                    "SEO Page Title",

                "priority":
                    "Medium",

                "evidence":
                    "Homepage title missing.",

                "impact":
                    (
                        "Search engines may struggle to "
                        "understand page relevance."
                    ),

                "recommendation":
                    "Create an optimized page title."

            })

        # ----------------------------------------------

        if not report.get("meta_description"):

            findings.append({

                "title":
                    "Meta Description",

                "priority":
                    "Medium",

                "evidence":
                    "Homepage meta description missing.",

                "impact":
                    (
                        "Lower click-through rates from "
                        "Google search results."
                    ),

                "recommendation":
                    "Write an optimized meta description."

            })

        return findings