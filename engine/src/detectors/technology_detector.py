class TechnologyDetector:
    """
    Detects the technology used by a website.
    """

    def detect(self, html):

        html = html.lower()

        # WordPress
        if "wp-content" in html or "wp-includes" in html:
            return "WordPress"

        # Shopify
        if "cdn.shopify.com" in html or "shopify" in html:
            return "Shopify"

        # Wix
        if "wixstatic.com" in html or "_wixcss" in html:
            return "Wix"

        # Squarespace
        if "static.squarespace.com" in html or "squarespace" in html:
            return "Squarespace"

        # Webflow
        if "webflow" in html:
            return "Webflow"

        # Joomla
        if "/media/system/" in html:
            return "Joomla"

        # Drupal
        if "drupal-settings-json" in html:
            return "Drupal"

        # React / Next.js
        if "__next" in html:
            return "Next.js"

        if "react" in html:
            return "React"

        return "Custom / Unknown"