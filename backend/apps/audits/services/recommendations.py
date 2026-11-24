"""
Recommendation Engine

Converts audit findings into structured business recommendations.
"""


def generate_recommendations(results):
    """
    Generate structured recommendations from audit results.
    """

    executive_summary = []

    critical = []
    high = []
    medium = []
    good = []

    # -------------------------------------------------
    # Security
    # -------------------------------------------------

    if results["ssl_enabled"]:

        good.append(
            "HTTPS is enabled, protecting visitor data."
        )

    else:

        critical.append(
            "Enable SSL/HTTPS immediately."
        )

    if results["https_redirect"]:

        good.append(
            "HTTP traffic correctly redirects to HTTPS."
        )

    else:

        high.append(
            "Redirect HTTP traffic to HTTPS."
        )

    # -------------------------------------------------
    # Performance
    # -------------------------------------------------

    load_time = results["load_time"]

    if load_time > 5:

        critical.append(
            f"Website loads slowly ({load_time:.2f}s). Improve page speed."
        )

    elif load_time > 3:

        high.append(
            f"Page load time is {load_time:.2f}s. Optimisation is recommended."
        )

    else:

        good.append(
            f"Good page loading speed ({load_time:.2f}s)."
        )

    # -------------------------------------------------
    # Images
    # -------------------------------------------------

    missing_alt = results["missing_alt_count"]

    if missing_alt > 0:

        high.append(
            f"Add ALT text to {missing_alt} images."
        )

    else:

        good.append(
            "All images contain ALT text."
        )

    # -------------------------------------------------
    # SEO
    # -------------------------------------------------

    if results["page_title"]:

        good.append(
            "Page title detected."
        )

    else:

        critical.append(
            "Missing page title."
        )

    if results["meta_description"]:

        good.append(
            "Meta description detected."
        )

    else:

        high.append(
            "Add a meta description."
        )

    if results["h1_count"] == 0:

        critical.append(
            "No H1 heading found."
        )

    elif results["h1_count"] > 1:

        medium.append(
            f"Multiple H1 headings detected ({results['h1_count']})."
        )

    else:

        good.append(
            "Exactly one H1 heading detected."
        )

    # -------------------------------------------------
    # Canonical
    # -------------------------------------------------

    if results["canonical_url"]:

        good.append(
            "Canonical URL configured."
        )

    else:

        medium.append(
            "Add a canonical URL."
        )

    # -------------------------------------------------
    # Viewport
    # -------------------------------------------------

    if results["has_viewport"]:

        good.append(
            "Viewport meta tag detected."
        )

    else:

        high.append(
            "Add a viewport meta tag."
        )

    # -------------------------------------------------
    # Open Graph
    # -------------------------------------------------

    if results["has_open_graph"]:

        good.append(
            "Open Graph tags configured."
        )

    else:

        medium.append(
            "Configure Open Graph tags."
        )

    # -------------------------------------------------
    # Twitter Card
    # -------------------------------------------------

    if results["has_twitter_card"]:

        good.append(
            "Twitter Card metadata detected."
        )

    else:

        medium.append(
            "Configure Twitter Card metadata."
        )

    # -------------------------------------------------
    # Technology-specific
    # -------------------------------------------------

    cms = results["cms"]

    if cms == "WordPress":

        medium.append(
            "Review installed plugins and keep WordPress core updated."
        )

    elif cms == "Shopify":

        medium.append(
            "Review installed apps to minimise unnecessary scripts."
        )

    elif cms == "Wix":

        medium.append(
            "Optimise media assets to improve Wix page performance."
        )

    # -------------------------------------------------
    # Executive Summary
    # -------------------------------------------------

    executive_summary.append(
        "The website has been analysed for security, SEO, performance, accessibility and technology."
    )

    if len(critical) == 0:

        executive_summary.append(
            "No critical issues were identified."
        )

    else:

        executive_summary.append(
            f"{len(critical)} critical issue(s) require attention."
        )

    if len(high):

        executive_summary.append(
            f"{len(high)} high-priority improvement(s) were identified."
        )

    return {
        "executive_summary": " ".join(executive_summary),
        "critical_issues": critical,
        "high_priority": high,
        "medium_priority": medium,
        "good_practices": good,
    }