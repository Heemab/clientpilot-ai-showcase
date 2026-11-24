from src.audit.base_audit import BaseAudit
from src.models.audit_result import AuditResult
from src.models.audit_finding import AuditFinding


class SecurityAudit(BaseAudit):
    """
    Evaluates the security posture of a website.
    """

    name = "Security Audit"

    def analyze(self, context):

        result = AuditResult(
            name=self.name,
            score=100,
        )

        # ------------------------------------------
        # HTTPS
        # ------------------------------------------

        if not context.url.lower().startswith("https://"):

            result.score -= 35

            result.add(
                AuditFinding(
                    category="Security",
                    severity="Critical",
                    title="Website is not using HTTPS",
                    description=(
                        "The website appears to be served over HTTP."
                    ),
                    business_impact=(
                        "Visitors may hesitate to submit enquiries "
                        "through an unsecured website."
                    ),
                    recommendation=(
                        "Install and correctly configure an SSL certificate."
                    ),
                    effort_hours=2,
                    estimated_value=300,
                )
            )

        # ------------------------------------------
        # Contact Form
        # ------------------------------------------

        if context.soup.find("form") is None:

            result.score -= 15

            result.add(
                AuditFinding(
                    category="Security",
                    severity="Medium",
                    title="No Contact Form Detected",
                    description=(
                        "No HTML form was found on the homepage."
                    ),
                    business_impact=(
                        "Potential customers may find it harder "
                        "to contact the business."
                    ),
                    recommendation=(
                        "Add a simple enquiry form."
                    ),
                    effort_hours=1,
                    estimated_value=250,
                )
            )

        # ------------------------------------------
        # Business Email
        # ------------------------------------------

        if "@" not in context.html:

            result.score -= 10

            result.add(
                AuditFinding(
                    category="Security",
                    severity="Medium",
                    title="No Business Email Detected",
                    description=(
                        "No email address was detected."
                    ),
                    business_impact=(
                        "Customers may question the business's credibility."
                    ),
                    recommendation=(
                        "Display a professional business email address."
                    ),
                    effort_hours=0.5,
                    estimated_value=100,
                )
            )

        if result.score < 0:
            result.score = 0

        return result