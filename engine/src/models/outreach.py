from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Outreach:
    """
    Represents a complete client outreach package.

    This model contains all communication generated
    for a prospect after a BusinessAssessment has
    been completed.

    It is the commercial counterpart to Proposal.
    """

    # --------------------------------------------------
    # Business Information
    # --------------------------------------------------

    business_name: str = ""

    contact_name: str = ""

    category: str = ""

    website: str = ""

    # --------------------------------------------------
    # Commercial Context
    # --------------------------------------------------

    priority: str = "MEDIUM"

    primary_service: str = ""

    estimated_value: int = 0

    roi_score: int = 0

    # --------------------------------------------------
    # Strategy
    # --------------------------------------------------

    strategy: str = ""

    call_to_action: str = ""

    # --------------------------------------------------
    # Email Sequence
    # --------------------------------------------------

    email_subject: str = ""

    email_body: str = ""

    follow_up_1: str = ""

    follow_up_2: str = ""

    follow_up_3: str = ""

    # --------------------------------------------------
    # Other Channels
    # --------------------------------------------------

    linkedin_message: str = ""

    whatsapp_message: str = ""

    call_script: str = ""

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    generated_at: datetime = field(
        default_factory=datetime.now
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @property
    def has_email(self) -> bool:

        return bool(self.email_body.strip())

    @property
    def has_followups(self) -> bool:

        return any(

            [

                self.follow_up_1,

                self.follow_up_2,

                self.follow_up_3,

            ]

        )

    @property
    def has_linkedin(self) -> bool:

        return bool(
            self.linkedin_message.strip()
        )

    @property
    def has_whatsapp(self) -> bool:

        return bool(
            self.whatsapp_message.strip()
        )

    @property
    def has_call_script(self) -> bool:

        return bool(
            self.call_script.strip()
        )