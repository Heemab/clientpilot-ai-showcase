from json import dumps

from src.analyzers.website_analyzer import WebsiteAnalyzer
from src.scoring.opportunity_scorer import OpportunityScorer
from src.intelligence.business_intelligence import BusinessIntelligence
from src.intelligence.findings_builder import FindingsBuilder
from src.intelligence.assessment_engine import AssessmentEngine
from src.services.contact_intelligence import ContactIntelligence

class OpportunityProcessor:
    """
    Coordinates opportunity enrichment.

    Processing Pipeline
    -------------------
    Website
        ↓
    WebsiteAnalyzer
        ↓
    WebsiteReport
        ↓
    AssessmentEngine
        ↓
    BusinessAssessment
        ↓
    BusinessIntelligence (legacy compatibility)
        ↓
    Opportunity
    """

    def __init__(self):

        self.website_analyzer = WebsiteAnalyzer()

        self.business_intelligence = BusinessIntelligence()

        self.findings_builder = FindingsBuilder()

        self.assessment_engine = AssessmentEngine()

        self.contact_intelligence = ContactIntelligence()

    # --------------------------------------------------
    # Main Processing
    # --------------------------------------------------

    def process(
        self,
        opportunity,
        verbose=False,
    ):

        # --------------------------------------------------
        # Website Analysis
        # --------------------------------------------------

        # --------------------------------------------------
        # Website Analysis
        # --------------------------------------------------

        try:

            report = self.website_analyzer.analyze(
                opportunity.website
            )

        except Exception as e:

            print(
                f"\n⚠ Website analysis failed for "
                f"{opportunity.business_name}"
            )

            print(f"Reason: {e}")

            # Minimal fallback report so the pipeline continues
            report = {

                "technology": "Unknown",

                "structured_report": None,

            }

        opportunity.website_report = report

        # --------------------------------------------------
        # Contact Intelligence
        # --------------------------------------------------

        contact = self.contact_intelligence.discover(
            opportunity.website
        )

        opportunity.business_email = (
        contact.business_email
        )

        opportunity.contact_page = (
        contact.contact_page
        )

        # --------------------------------------------------
        # Structured Website Report
        # --------------------------------------------------

        structured_report = report.get(
            "structured_report"
        )

        # --------------------------------------------------
        # Business Assessment
        # --------------------------------------------------

        if structured_report is not None:

            assessment = self.assessment_engine.assess(
                structured_report
            )

            opportunity.business_assessment = assessment

        else:

            assessment = None

            opportunity.business_assessment = None

        # --------------------------------------------------
        # Legacy Findings
        # --------------------------------------------------

        try:

            opportunity.website_findings = (
                self.findings_builder.build(report)
            )

            opportunity.website_structured_findings = (
                self.findings_builder.build_structured(
                    report
                )
            )

        except Exception:

            opportunity.website_findings = []

            opportunity.website_structured_findings = []

        # --------------------------------------------------
        # Persist JSON
        # --------------------------------------------------

        report_copy = dict(report)

        if "structured_report" in report_copy:

            report_copy["structured_report"] = None

        opportunity.website_report_json = dumps(
            report_copy,
            ensure_ascii=False,
        )

        opportunity.website_findings_json = dumps(
            opportunity.website_findings,
            ensure_ascii=False,
        )

        opportunity.website_structured_findings_json = dumps(
            opportunity.website_structured_findings,
            ensure_ascii=False,
        )

        # --------------------------------------------------
        # Technology
        # --------------------------------------------------

        opportunity.technology = report.get(
            "technology",
            "Unknown",
        )


        # --------------------------------------------------
        # Legacy Business Intelligence
        # (Temporary compatibility layer)
        # --------------------------------------------------

        try:

            intelligence = self.business_intelligence.analyze(
                opportunity,
                report,
            )

        except Exception:

            intelligence = {

                "priority": "LOW",

                "recommended_services": [],

                "primary_service": "",

                "estimated_value": 0,

                "estimated_hours": 0,

                "difficulty": "Unknown",

                "closing_probability": 0,

                "roi_score": 0,

                "reason": (
                    "Website could not be analysed."
                ),

            }

        # --------------------------------------------------
        # Merge Assessment
        # --------------------------------------------------

        if assessment is not None:

            opportunity.priority = (
                assessment.priority
            )

            opportunity.recommended_services = ", ".join(
                assessment.recommended_services
            )

            opportunity.primary_service = (
                assessment.primary_service
            )

            opportunity.estimated_value = (
                assessment.estimated_value
            )

            opportunity.estimated_hours = (
                assessment.estimated_hours
            )

            opportunity.difficulty = (
                assessment.difficulty
            )

            opportunity.roi_score = (
                assessment.roi_score
            )

            opportunity.closing_probability = (
                assessment.closing_probability
            )

            opportunity.sales_reason = (
                assessment.summary
            )

        else:

            opportunity.priority = (
                intelligence["priority"]
            )

            opportunity.recommended_services = ", ".join(
                intelligence["recommended_services"]
            )

            opportunity.primary_service = (
                intelligence["primary_service"]
            )

            opportunity.estimated_value = (
                intelligence["estimated_value"]
            )

            opportunity.estimated_hours = (
                intelligence["estimated_hours"]
            )

            opportunity.difficulty = (
                intelligence["difficulty"]
            )

            opportunity.closing_probability = (
                intelligence["closing_probability"]
            )

            opportunity.roi_score = (
                intelligence["roi_score"]
            )

            opportunity.sales_reason = (
                intelligence["reason"]
            )

        # --------------------------------------------------
        # Console Summary
        # --------------------------------------------------

        if verbose:
            self._print_summary(
                opportunity,
                 intelligence,
            )

        return opportunity

    # --------------------------------------------------
    # Console Output
    # --------------------------------------------------

    def _print_summary(
        self,
        opportunity,
        intelligence,
    ):

        print()

        print("=" * 60)

        print(opportunity.business_name)

        print("=" * 60)

        print(
            f"Technology        : {opportunity.technology}"
        )

        print(
            f"Opportunity Score : {opportunity.opportunity_score}"
        )

        print(
            f"Priority          : {opportunity.priority}"
        )

        print(
            f"Primary Service   : {opportunity.primary_service}"
        )

        print(
            f"Estimated Value   : ${opportunity.estimated_value:,}"
        )

        print(
            f"Estimated Hours   : {opportunity.estimated_hours}"
        )

        print(
            f"Difficulty        : {opportunity.difficulty}"
        )

        print(
            f"ROI Score         : {opportunity.roi_score}"
        )

        print(
            f"Closing Chance    : {opportunity.closing_probability}%"
        )

        print()

        print("Website Findings")

        print("----------------")

        if opportunity.website_findings:

            for finding in opportunity.website_findings:

                print(f"• {finding}")

        else:

            print("• None")

        print()

        print("Structured Findings")

        print("-------------------")

        if opportunity.website_structured_findings:

            for finding in (
                opportunity.website_structured_findings
            ):

                print(
                    f"• {finding['title']} "
                    f"[{finding['priority']}]"
                )

        else:

            print("• None")

        print()

        print("Recommended Services")

        print("--------------------")

        services = (
            opportunity.recommended_services.split(",")
            if opportunity.recommended_services
            else []
        )

        for service in services:

            if service.strip():

                print(f"✓ {service.strip()}")

        print()

        print("Sales Summary")

        print("-------------")

        print(opportunity.sales_reason)

        print()

        print("=" * 60)