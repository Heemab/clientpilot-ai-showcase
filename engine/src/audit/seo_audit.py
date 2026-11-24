from src.audit.base_audit import BaseAudit
from src.models.audit_result import AuditResult
from src.models.audit_finding import AuditFinding


class SEOAudit(BaseAudit):
    """
    Performs a basic on-page SEO audit.
    """

    name = "SEO Audit"

    def analyze(self, context):

        result = AuditResult(
            name=self.name,
            score=100,
        )

        soup = context.soup

        # --------------------------------------------------
        # Metrics
        # --------------------------------------------------

        result.metrics = {
            "title": "",
            "meta_description": False,
            "h1_count": 0,
            "technology": "Unknown",
        }

        # --------------------------------------------------
        # Page Title
        # --------------------------------------------------

        title = ""

        if soup.title:
            title = soup.title.text.strip()

        result.metrics["title"] = title

        if not title:

            result.score -= 20

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Critical",
                    title="Missing Page Title",
                    description="The homepage does not contain a <title> tag.",
                    business_impact=(
                        "Search engines rely on page titles "
                        "to understand page content."
                    ),
                    recommendation="Add a descriptive page title.",
                    effort_hours=0.5,
                    estimated_value=150,
                )
            )

        elif len(title) < 20:

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Page Title Too Short",
                    description="The page title is shorter than recommended.",
                    business_impact="A short title may reduce search relevance.",
                    recommendation="Increase the title to 20–60 characters.",
                )
            )

        elif len(title) > 60:

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Page Title Too Long",
                    description="The page title exceeds 60 characters.",
                    business_impact="Search engines may truncate the title.",
                    recommendation="Reduce the title length.",
                )
            )

        # --------------------------------------------------
        # Meta Description
        # --------------------------------------------------

        meta = soup.find(
            "meta",
            attrs={"name": "description"},
        )

        description = ""

        if meta:
            description = meta.get("content", "").strip()

        result.metrics["meta_description"] = bool(description)

        if not description:

            result.score -= 20

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="High",
                    title="Missing Meta Description",
                    description="No meta description was found.",
                    business_impact=(
                        "Search engines may generate poor snippets."
                    ),
                    recommendation="Add a unique meta description.",
                    effort_hours=0.5,
                    estimated_value=150,
                )
            )

        # --------------------------------------------------
        # H1
        # --------------------------------------------------

        h1_tags = soup.find_all("h1")

        result.metrics["h1_count"] = len(h1_tags)

        if len(h1_tags) == 0:

            result.score -= 15

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Medium",
                    title="Missing H1 Heading",
                    description="No H1 heading was found.",
                    business_impact="Search engines use H1 headings to identify page topics.",
                    recommendation="Add one clear H1 heading.",
                )
            )

        elif len(h1_tags) > 1:

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Multiple H1 Headings",
                    description="Multiple H1 headings were detected.",
                    business_impact="Multiple H1s may reduce content clarity.",
                    recommendation="Use a single H1 heading.",
                )
            )

        # --------------------------------------------------
        # HTML Language
        # --------------------------------------------------

        html_tag = soup.find("html")

        if html_tag and not html_tag.get("lang"):

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Missing HTML Language",
                    description="The HTML element has no language attribute.",
                    business_impact="Search engines may not correctly determine page language.",
                    recommendation="Add a lang attribute to the HTML tag.",
                )
            )

        # --------------------------------------------------
        # Charset
        # --------------------------------------------------

        charset = soup.find("meta", attrs={"charset": True})

        if charset is None:

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Missing Charset Declaration",
                    description="No charset declaration was detected.",
                    business_impact="Character encoding issues may occur.",
                    recommendation="Declare UTF-8 in the document head.",
                )
            )

        # --------------------------------------------------
        # Open Graph
        # --------------------------------------------------

        og = soup.find(
            "meta",
            attrs={"property": "og:title"},
        )

        if og is None:

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Open Graph Metadata Missing",
                    description="Open Graph tags were not detected.",
                    business_impact="Social sharing previews may be incomplete.",
                    recommendation="Add Open Graph metadata.",
                )
            )

        # --------------------------------------------------
        # Twitter Card
        # --------------------------------------------------

        twitter = soup.find(
            "meta",
            attrs={"name": "twitter:card"},
        )

        if twitter is None:

            result.score -= 5

            result.add(
                AuditFinding(
                    category="SEO",
                    severity="Low",
                    title="Twitter Card Metadata Missing",
                    description="Twitter Card tags were not detected.",
                    business_impact="Shared links may display poorly on X/Twitter.",
                    recommendation="Add Twitter Card metadata.",
                )
            )

        # --------------------------------------------------
        # Technology Detection
        # --------------------------------------------------

        html = context.html.lower()

        if "wp-content" in html or "wordpress" in html:
            result.metrics["technology"] = "WordPress"

        elif "cdn.shopify.com" in html or "shopify" in html:
            result.metrics["technology"] = "Shopify"

        elif "wixstatic.com" in html or "wix.com" in html:
            result.metrics["technology"] = "Wix"

        if result.score < 0:
            result.score = 0

        return result