import re


def detect_technology(response, soup):
    """
    Detect CMS, themes, frameworks, analytics and marketing tools.
    """

    technologies = []

    cms = "Unknown"

    theme = "Unknown"

    html = str(soup).lower()

    headers = {
        k.lower(): v.lower()
        for k, v in response.headers.items()
    }

    # ---------------------------------------------------------
    # Server
    # ---------------------------------------------------------

    server = headers.get("server", "")

    if "cloudflare" in server:
        technologies.append("Cloudflare")

    # ---------------------------------------------------------
    # Generator Meta Tag
    # ---------------------------------------------------------

    generator = soup.find(
        "meta",
        attrs={"name": "generator"},
    )

    if generator:

        content = generator.get(
            "content",
            "",
        ).lower()

        if "wordpress" in content:
            cms = "WordPress"

        elif "drupal" in content:
            cms = "Drupal"

        elif "joomla" in content:
            cms = "Joomla"

        elif "shopify" in content:
            cms = "Shopify"

        elif "wix" in content:
            cms = "Wix"

    # ---------------------------------------------------------
    # CMS Detection
    # ---------------------------------------------------------

    if "/wp-content/" in html:

        cms = "WordPress"

        technologies.append("WordPress")

        theme_match = re.search(
            r"/wp-content/themes/([^/]+)/",
            html,
        )

        if theme_match:

            theme = (
                theme_match.group(1)
                .replace("-", " ")
                .title()
            )

    elif (
        "static.wixstatic.com" in html
        or "wixstatic.com" in html
        or "static.parastorage.com" in html
    ):

        cms = "Wix"

        technologies.append("Wix")

    elif "cdn.shopify.com" in html:

        cms = "Shopify"

        technologies.append("Shopify")

    elif "static.squarespace.com" in html:

        cms = "Squarespace"

        technologies.append("Squarespace")

    # ---------------------------------------------------------
    # WordPress Plugins
    # ---------------------------------------------------------

    if cms == "WordPress":

        if (
            "elementor-frontend"
            in html
            or "/plugins/elementor/"
            in html
        ):

            technologies.append("Elementor")

        if "woocommerce" in html:

            technologies.append("WooCommerce")

    # ---------------------------------------------------------
    # Frameworks
    # ---------------------------------------------------------

    if "_next/" in html:
        technologies.append("Next.js")

    if "react" in html:
        technologies.append("React")

    if "vue" in html:
        technologies.append("Vue.js")

    if "angular" in html:
        technologies.append("Angular")

    if "bootstrap.min.css" in html:
        technologies.append("Bootstrap")

    if "tailwind" in html:
        technologies.append("Tailwind CSS")

    # ---------------------------------------------------------
    # Analytics
    # ---------------------------------------------------------

    if (
        "gtag(" in html
        or "google-analytics" in html
        or "googletagmanager" in html
    ):

        technologies.append("Google Analytics")

    if "gtm.js" in html:

        technologies.append("Google Tag Manager")

    if "connect.facebook.net" in html:

        technologies.append("Facebook Pixel")

    if "hotjar" in html:

        technologies.append("Hotjar")

    if "clarity.ms" in html:

        technologies.append("Microsoft Clarity")

    # ---------------------------------------------------------
    # Fonts
    # ---------------------------------------------------------

    if "fonts.googleapis.com" in html:

        technologies.append("Google Fonts")

    if (
        "font-awesome" in html
        or "fontawesome" in html
    ):

        technologies.append("Font Awesome")

    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------

    technologies = sorted(set(technologies))

    return {
        "cms": cms,
        "theme": theme,
        "technologies": technologies,
    }