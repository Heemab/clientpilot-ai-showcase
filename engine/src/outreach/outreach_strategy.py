from dataclasses import dataclass

from src.models.business_assessment import BusinessAssessment


@dataclass(slots=True)
class OutreachStrategy:
    """
    Determines the outreach approach based on
    a BusinessAssessment.

    This class contains no formatting.

    It simply decides HOW the AI should sell.
    """

    tone: str

    opening: str

    focus: str

    call_to_action: str

    email_length: str


class OutreachStrategyEngine:
    """
    Creates an outreach strategy from a
    BusinessAssessment.
    """

    def build(
        self,
        assessment: BusinessAssessment,
    ) -> OutreachStrategy:

        # ------------------------------------------
        # High Priority
        # ------------------------------------------

        if assessment.priority == "HIGH":

            return OutreachStrategy(

                tone="Urgent but Professional",

                opening=(
                    "I noticed a few issues on your website "
                    "that may be costing enquiries."
                ),

                focus=(
                    "Lead with the highest-impact business problem."
                ),

                call_to_action=(
                    "Offer a free 20-minute review."
                ),

                email_length="Short",

            )

        # ------------------------------------------
        # Medium Priority
        # ------------------------------------------

        if assessment.priority == "MEDIUM":

            return OutreachStrategy(

                tone="Helpful",

                opening=(
                    "I recently reviewed your website and "
                    "identified a few opportunities to improve "
                    "customer acquisition."
                ),

                focus=(
                    "Highlight quick wins and ROI."
                ),

                call_to_action=(
                    "Invite them to discuss the findings."
                ),

                email_length="Medium",

            )

        # ------------------------------------------
        # Low Priority
        # ------------------------------------------

        return OutreachStrategy(

            tone="Educational",

            opening=(
                "Your website already performs well. "
                "I found a few areas that could make it even stronger."
            ),

            focus=(
                "Focus on optimisation."
            ),

            call_to_action=(
                "Offer an optimisation consultation."
            ),

            email_length="Short",

        )