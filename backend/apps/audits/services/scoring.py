"""
Website Audit Scoring Engine
"""


def calculate_scores(results):
    """
    Calculate category scores and an overall weighted score.
    """

    # ==========================================================
    # SEO Score
    # ==========================================================

    seo_score = 0

    if results["page_title"]:
        seo_score += 15

    if results["meta_description"]:
        seo_score += 15

    if results["h1_count"] == 1:
        seo_score += 15

    if results["canonical_url"]:
        seo_score += 10

    if results["has_viewport"]:
        seo_score += 10

    if results["has_open_graph"]:
        seo_score += 10

    if results["has_twitter_card"]:
        seo_score += 5

    if results["html_lang"]:
        seo_score += 5

    if results["has_favicon"]:
        seo_score += 5

    # Image ALT score (10 pts)

    if results["image_count"] > 0:

        missing_ratio = (
            results["missing_alt_count"] / results["image_count"]
        )

        seo_score += max(
            0,
            round(10 * (1 - missing_ratio)),
        )
    else:
        seo_score += 10

    seo_score = min(100, seo_score)

    results["seo_score"] = seo_score

    # ==========================================================
    # Performance Score
    # ==========================================================

    load = results["load_time"]

    if load <= 1:
        performance = 100
    elif load <= 2:
        performance = 90
    elif load <= 3:
        performance = 80
    elif load <= 4:
        performance = 70
    elif load <= 5:
        performance = 60
    elif load <= 6:
        performance = 40
    elif load <= 8:
        performance = 20
    else:
        performance = 10

    results["performance_score"] = performance

    # ==========================================================
    # Accessibility Score
    #
    # Temporary implementation until full accessibility
    # analyser is added.
    # ==========================================================

    accessibility = 100

    if results["missing_alt_count"] > 0:
        accessibility -= min(
            30,
            results["missing_alt_count"] * 5,
        )

    if not results["html_lang"]:
        accessibility -= 20

    if not results["has_viewport"]:
        accessibility -= 20

    accessibility = max(0, accessibility)

    results["accessibility_score"] = accessibility

    # ==========================================================
    # Security Score
    # ==========================================================

    security = 0

    if results["ssl_enabled"]:
        security += 50

    if results["https_redirect"]:
        security += 50

    # ==========================================================
    # Overall Score
    # ==========================================================

    overall = round(
        (
            seo_score * 0.40
            + performance * 0.25
            + accessibility * 0.20
            + security * 0.15
        )
    )

    results["overall_score"] = overall

    return results