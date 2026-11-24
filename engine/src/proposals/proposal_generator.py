from datetime import datetime


class ProposalGenerator:
    """
    Generates a structured proposal from an Opportunity.

    ProposalGenerator prepares presentation data only.

    It prefers BusinessAssessment (new architecture)
    and falls back to legacy opportunity fields when
    required for backward compatibility.
    """

    def __init__(self):
        pass

    # --------------------------------------------------
    # Generate Proposal
    # --------------------------------------------------

    def generate(
        self,
        opportunity,
        scoring_result=None,
    ):

        assessment = getattr(
            opportunity,
            "business_assessment",
            None,
        )

        # --------------------------------------------------
        # Legacy Findings
        # --------------------------------------------------

        legacy_findings = getattr(
            opportunity,
            "website_findings",
            [],
        )

        # --------------------------------------------------
        # Legacy Structured Findings
        # --------------------------------------------------

        structured_findings = getattr(
            opportunity,
            "website_structured_findings",
            [],
        )

        # --------------------------------------------------
        # Business Assessment
        # --------------------------------------------------

        if assessment:

            priority = assessment.priority

            investment = assessment.estimated_value

            estimated_hours = assessment.estimated_hours

            difficulty = assessment.difficulty

            roi_score = assessment.roi_score

            closing_probability = (
                assessment.closing_probability
            )

            sales_reason = assessment.summary

            services = assessment.recommended_services

            business_insights = (
                assessment.business_opportunities
            )

        else:

            priority = getattr(
                opportunity,
                "priority",
                "Medium",
            )

            investment = getattr(
                opportunity,
                "estimated_value",
                0,
            )

            estimated_hours = getattr(
                opportunity,
                "estimated_hours",
                0,
            )

            difficulty = getattr(
                opportunity,
                "difficulty",
                "Unknown",
            )

            roi_score = getattr(
                opportunity,
                "roi_score",
                0,
            )

            closing_probability = getattr(
                opportunity,
                "closing_probability",
                0,
            )

            sales_reason = getattr(
                opportunity,
                "sales_reason",
                "",
            )

            services = []

            recommended = getattr(
                opportunity,
                "recommended_services",
                "",
            )

            if recommended:

                services = [

                    service.strip()

                    for service in recommended.split(",")

                    if service.strip()

                ]

            business_insights = structured_findings

        # --------------------------------------------------
        # Override with Scoring Result
        # --------------------------------------------------

        if scoring_result is not None:

            priority = scoring_result.priority

            roi_score = scoring_result.score

            investment = scoring_result.estimated_revenue

            services = scoring_result.recommended_services

            sales_reason = "\n".join(
                f"- {reason}"
                for reason in scoring_result.reasoning
            )

        # --------------------------------------------------
        # Proposal
        # --------------------------------------------------

        proposal = {

            # ------------------------------------------
            # Metadata
            # ------------------------------------------

            "generated_at":
                datetime.now().strftime(
                    "%d %B %Y"
                ),

            # ------------------------------------------
            # Business
            # ------------------------------------------

            "business_name":
                opportunity.business_name,

            "category":
                opportunity.category,

            "website":
                opportunity.website,

            "technology":
                getattr(
                    opportunity,
                    "technology",
                    "Unknown",
                ),

            "priority":
                priority,

            "opportunity_score":
                (
                    scoring_result.score
                    if scoring_result is not None
                    else getattr(
                        opportunity,
                        "opportunity_score",
                        roi_score,
                    )
                ),

            # ------------------------------------------
            # Executive Summary
            # ------------------------------------------

            "executive_summary":
                self._executive_summary(
                    opportunity
                ),

            # ------------------------------------------
            # Findings
            # ------------------------------------------

            "website_findings":
                legacy_findings,

            "business_insights":
                business_insights,

            # ------------------------------------------
            # Recommendations
            # ------------------------------------------

            "recommended_services":
                services,

            # ------------------------------------------
            # Commercial Assessment
            # ------------------------------------------

            "investment":
                investment,

            "estimated_hours":
                estimated_hours,

            "difficulty":
                difficulty,

            "closing_probability":
                closing_probability,

            "roi_score":
                roi_score,

            "sales_reason":
                sales_reason,

            # ------------------------------------------
            # Timeline
            # ------------------------------------------

            "timeline":
                self._timeline(
                    estimated_hours
                ),

            # ------------------------------------------
            # Outcomes
            # ------------------------------------------

            "expected_results":
                self._expected_results(),

            "next_steps":
                self._next_steps(),

        }

        return proposal

    # --------------------------------------------------
    # Executive Summary
    # --------------------------------------------------

    def _executive_summary(
        self,
        opportunity,
    ):

        return (

            f"We reviewed "
            f"{opportunity.business_name}'s "
            f"online presence and identified "
            f"several opportunities to improve "
            f"customer acquisition, search "
            f"visibility and enquiry generation. "
            f"The recommendations in this proposal "
            f"focus on practical improvements that "
            f"deliver measurable business results."

        )

    # --------------------------------------------------
    # Timeline
    # --------------------------------------------------

    def _timeline(
        self,
        hours,
    ):

        if hours <= 8:

            return "Approximately 1 week"

        elif hours <= 20:

            return "Approximately 2–3 weeks"

        elif hours <= 40:

            return "Approximately 1 month"

        return "Timeline to be confirmed"

    # --------------------------------------------------
    # Expected Results
    # --------------------------------------------------

    def _expected_results(self):

        return [

            "Improve customer trust",

            "Increase website enquiries",

            "Improve Google visibility",

            "Strengthen online presence",

            "Create a better customer experience",

        ]

    # --------------------------------------------------
    # Next Steps
    # --------------------------------------------------

    def _next_steps(self):

        return (

            "Schedule a 20-minute discovery call "
            "to review these findings, prioritise "
            "the improvements and agree on an "
            "implementation roadmap."

        )