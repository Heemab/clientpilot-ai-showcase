def analyze_seo(soup):
    """
    Advanced on-page SEO analysis.
    """

    result = {
        "page_title": "",
        "meta_description": "",
        "h1_count": 0,
        "h2_count": 0,
        "image_count": 0,
        "missing_alt_count": 0,
        "canonical_url": "",
        "has_viewport": False,
        "has_open_graph": False,
        "has_twitter_card": False,
        "html_lang": "",
        "has_favicon": False,
    }

    # -------------------------
    # Title
    # -------------------------

    if soup.title:
        result["page_title"] = soup.title.get_text(strip=True)

    # -------------------------
    # Meta Description
    # -------------------------

    meta = soup.find(
        "meta",
        attrs={"name": "description"},
    )

    if meta:
        result["meta_description"] = meta.get(
            "content",
            "",
        ).strip()

    # -------------------------
    # H1 / H2
    # -------------------------

    result["h1_count"] = len(soup.find_all("h1"))
    result["h2_count"] = len(soup.find_all("h2"))

    # -------------------------
    # Images
    # -------------------------

    images = soup.find_all("img")

    result["image_count"] = len(images)

    result["missing_alt_count"] = sum(
        1
        for img in images
        if not img.get("alt", "").strip()
    )

    # -------------------------
    # Canonical
    # -------------------------

    canonical = soup.find(
        "link",
        rel="canonical",
    )

    if canonical:
        result["canonical_url"] = canonical.get(
            "href",
            "",
        )

    # -------------------------
    # Viewport
    # -------------------------

    viewport = soup.find(
        "meta",
        attrs={"name": "viewport"},
    )

    result["has_viewport"] = viewport is not None

    # -------------------------
    # Open Graph
    # -------------------------

    og = soup.find(
        "meta",
        attrs={"property": "og:title"},
    )

    result["has_open_graph"] = og is not None

    # -------------------------
    # Twitter Card
    # -------------------------

    twitter = soup.find(
        "meta",
        attrs={"name": "twitter:card"},
    )

    result["has_twitter_card"] = twitter is not None

    # -------------------------
    # HTML lang
    # -------------------------

    html = soup.find("html")

    if html:
        result["html_lang"] = html.get(
            "lang",
            "",
        )

    # -------------------------
    # Favicon
    # -------------------------

    favicon = soup.find(
        "link",
        rel=lambda value: value and "icon" in value.lower(),
    )

    result["has_favicon"] = favicon is not None

    return result