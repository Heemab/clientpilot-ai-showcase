from src.models.business_assessment import BusinessAssessment


class AssessmentEngine:
    """
    Converts a WebsiteReport into a BusinessAssessment.

    The AssessmentEngine transforms technical audit
    findings into commercial recommendations that can
    be consumed by proposals, CRM and dashboards.
    """

    # --------------------------------------------------

    def assess(self, report):

        assessment = BusinessAssessment()

        assessment.overall_score = report.overall_score

        assessment.findings = []

        assessment.business_opportunities = []

        # --------------------------------------------------
        # Collect Findings
        # --------------------------------------------------

        audits = []

        if getattr(report, "security", None):

            audits.append(report.security)

        if getattr(report, "seo", None):

            audits.append(report.seo)

        for audit in audits:

            for finding in audit.findings:

                assessment.findings.append(finding)

                assessment.business_opportunities.append(

                    {

                        "category":
                            finding.category,

                        "title":
                            finding.title,

                        "priority":
                            finding.severity,

                        "impact":
                            finding.business_impact,

                        "recommendation":
                            finding.recommendation,

                        "estimated_value":
                            finding.estimated_value,

                        "effort_hours":
                            finding.effort_hours,

                    }

                )

        # --------------------------------------------------
        # Priority
        # --------------------------------------------------

        if assessment.overall_score < 50:

            assessment.priority = "HIGH"

        elif assessment.overall_score < 75:

            assessment.priority = "MEDIUM"

        else:

            assessment.priority = "LOW"

        # --------------------------------------------------
        # Recommended Services
        # --------------------------------------------------

        services = set()

        for finding in assessment.findings:

            if finding.category == "Security":

                services.add("SSL Installation")

                services.add("Security Audit")

            elif finding.category == "SEO":

                services.add("SEO Optimisation")

                services.add("Technical SEO")

        assessment.recommended_services = sorted(services)

        if assessment.recommended_services:

            assessment.primary_service = (
                assessment.recommended_services[0]
            )

        # --------------------------------------------------
        # Commercial Estimates
        # --------------------------------------------------

        total_hours = 0

        total_value = 0

        for finding in assessment.findings:

            total_hours += (
                finding.effort_hours or 1
            )

            total_value += (
                finding.estimated_value or 100
            )

        assessment.estimated_hours = max(
            4,
            total_hours,
        )

        assessment.estimated_value = max(
            500,
            total_value,
        )

        assessment.roi_score = min(
            500,
            assessment.estimated_value // 10,
        )

        assessment.closing_probability = max(
            25,
            100 - assessment.overall_score,
        )

        assessment.summary = (

            f"The website achieved an overall "

            f"digital score of "

            f"{assessment.overall_score}/100. "

            f"{len(assessment.findings)} "

            f"improvement opportunities were "

            f"identified across security and SEO."

        )

        return assessment