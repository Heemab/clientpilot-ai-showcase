"""
Effort Estimation Engine

Estimate implementation effort for each
recommended service.
"""


def estimate_effort(service, results):
    """
    Returns estimated hours required.
    """

    # -----------------------------------------
    # Website Speed
    # -----------------------------------------

    if service == "Website Speed Optimisation":

        load_time = results["load_time"]

        if load_time >= 8:
            return 16

        if load_time >= 6:
            return 12

        if load_time >= 4:
            return 8

        return 5

    # -----------------------------------------
    # SEO
    # -----------------------------------------

    if service == "SEO Optimisation":

        missing_alt = results["missing_alt_count"]

        if missing_alt > 200:
            return 12

        if missing_alt > 100:
            return 8

        if missing_alt > 20:
            return 5

        return 3

    # -----------------------------------------
    # Technical SEO
    # -----------------------------------------

    if service == "Technical SEO":
        return 2

    # -----------------------------------------
    # On-page SEO
    # -----------------------------------------

    if service == "On-page SEO":
        return 3

    # -----------------------------------------
    # SSL
    # -----------------------------------------

    if service == "SSL Installation":
        return 2

    if service == "HTTPS Redirect Configuration":
        return 1

    # -----------------------------------------
    # Accessibility
    # -----------------------------------------

    if service == "Accessibility Compliance":
        return 4

    # -----------------------------------------
    # Social Metadata
    # -----------------------------------------

    if service == "Social Media Optimisation":
        return 2

    if service == "Twitter Card Optimisation":
        return 1

    # -----------------------------------------
    # Care Plan
    # -----------------------------------------

    if service == "Website Care Plan":
        return 1

    return 2