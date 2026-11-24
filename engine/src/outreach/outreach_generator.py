from src.models.outreach import Outreach
from src.outreach.outreach_strategy import (
    OutreachStrategyEngine,
)


class OutreachGenerator:
    """
    Generates a complete Outreach object from an
    Opportunity and its BusinessAssessment.
    """

    def __init__(self):

        self.strategy_engine = (
            OutreachStrategyEngine()
        )

    # --------------------------------------------------
    # Generate Outreach
    # --------------------------------------------------

    def generate(
        self,
        opportunity,
    ):

        assessment = opportunity.business_assessment

        if assessment is None:

            raise ValueError(
                "Opportunity has no BusinessAssessment."
            )

        strategy = self.strategy_engine.build(
            assessment
        )

        outreach = Outreach(

            business_name=opportunity.business_name,

            category=opportunity.category,

            website=opportunity.website,

            priority=assessment.priority,

            primary_service=assessment.primary_service,

            estimated_value=assessment.estimated_value,

            roi_score=assessment.roi_score,

            strategy=strategy.focus,

            call_to_action=strategy.call_to_action,

            email_subject=self._subject(
                opportunity,
                assessment,
            ),

            email_body=self._email(
                opportunity,
                assessment,
                strategy,
            ),

            follow_up_1=self._followup1(
                opportunity,
            ),

            follow_up_2=self._followup2(
                opportunity,
            ),

            follow_up_3=self._followup3(
                opportunity,
            ),

            linkedin_message=self._linkedin(
                opportunity,
            ),

            whatsapp_message=self._whatsapp(
                opportunity,
            ),

            call_script=self._call_script(
                opportunity,
            ),

        )

        return outreach

    # --------------------------------------------------

    def _subject(
        self,
        opportunity,
        assessment,
    ):

        return (
            f"{opportunity.business_name}: "
            f"{assessment.primary_service} Opportunity"
        )

    # --------------------------------------------------

    def _email(
        self,
        opportunity,
        assessment,
        strategy,
    ):

        return f"""
Hello,

{strategy.opening}

While reviewing {opportunity.business_name}'s website, I identified several opportunities that could improve customer trust and generate more enquiries.

My primary recommendation is:

• {assessment.primary_service}

Based on the assessment, these improvements have an estimated implementation value of ${assessment.estimated_value:,}.

{strategy.call_to_action}

Kind regards,

ClientPilot
AI Client Acquisition Engine
""".strip()

    # --------------------------------------------------

    def _followup1(
        self,
        opportunity,
    ):

        return (
            f"Hello,\n\n"
            f"I just wanted to follow up regarding the "
            f"website assessment I prepared for "
            f"{opportunity.business_name}. "
            f"Please let me know if you'd like me "
            f"to send a copy."
        )

    # --------------------------------------------------

    def _followup2(
        self,
        opportunity,
    ):

        return (
            f"Just checking in to see whether "
            f"you've had a chance to review my "
            f"previous message regarding "
            f"{opportunity.business_name}."
        )

    # --------------------------------------------------

    def _followup3(
        self,
        opportunity,
    ):

        return (
            f"This will be my final follow-up. "
            f"If improving your website becomes "
            f"a priority in the future, I'd be "
            f"happy to help."
        )

    # --------------------------------------------------

    def _linkedin(
        self,
        opportunity,
    ):

        return (
            f"Hi, I recently reviewed "
            f"{opportunity.business_name}'s website "
            f"and found a few opportunities that "
            f"could improve customer acquisition."
        )

    # --------------------------------------------------

    def _whatsapp(
        self,
        opportunity,
    ):

        return (
            f"Hello. I prepared a brief website "
            f"assessment for {opportunity.business_name}. "
            f"Would you like me to send it?"
        )

    # --------------------------------------------------

    def _call_script(
        self,
        opportunity,
    ):

        return (
            f"Introduce yourself, mention that "
            f"you reviewed {opportunity.business_name}'s "
            f"website, explain that you identified "
            f"a few improvement opportunities, "
            f"and ask whether they would be "
            f"interested in a free review."
        )