from textwrap import dedent


class AIOutreachGenerator:
    """
    Generates sales outreach for an opportunity.

    Version 1:
        Template-based.

    Version 2:
        AI (OpenAI / Claude / Local LLM).

    The rest of the application should never care
    how the content is generated.
    """

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def generate(self, opportunity):
        """
        Returns every outreach asset.
        """

        return {

            "email": self.generate_email(opportunity),

            "linkedin": self.generate_linkedin_message(
                opportunity
            ),

            "follow_up": self.generate_followup(
                opportunity
            ),

            "call_script": self.generate_call_script(
                opportunity
            ),

            "proposal_intro": self.generate_proposal_intro(
                opportunity
            ),

        }

    # --------------------------------------------------
    # Email
    # --------------------------------------------------

    def generate_email(self, opportunity):

        service = (
            opportunity.primary_service
            or "Website Improvement"
        )

        subject = (
            f"Quick idea for "
            f"{opportunity.business_name}"
        )

        body = dedent(f"""
        Hi,

        I came across {opportunity.business_name}
        while researching businesses in your area.

        I noticed there may be an opportunity to improve your website through
        {service.lower()}.

        Based on my analysis, this could improve
        your online visibility and help convert
        more visitors into customers.

        I'd be happy to provide a complimentary
        assessment outlining what I found and
        the improvements I'd recommend.

        Would you be open to a short conversation
        sometime next week?

        Best regards,
        """)

        return {

            "subject": subject,

            "body": body.strip(),

        }

    # --------------------------------------------------
    # LinkedIn
    # --------------------------------------------------

    def generate_linkedin_message(self, opportunity):

        service = (
            opportunity.primary_service
            or "website improvements"
        )

        return dedent(f"""
        Hi,

        I recently came across
        {opportunity.business_name}.

        I noticed a few opportunities around
        {service.lower()}.

        I'd be happy to share a few ideas if
        you're interested.

        Thanks!
        """).strip()

    # --------------------------------------------------
    # Follow-up
    # --------------------------------------------------

    def generate_followup(self, opportunity):

        return dedent(f"""
        Hi,

        Just checking whether you had a chance
        to read my previous message.

        I'd still be happy to provide a free
        website assessment for
        {opportunity.business_name}.

        Let me know if you'd like me to send it.

        Thanks!
        """).strip()

    # --------------------------------------------------
    # Call Script
    # --------------------------------------------------

    def generate_call_script(self, opportunity):

        service = (
            opportunity.primary_service
            or "website improvements"
        )

        return dedent(f"""
        Hello,

        My name is ...

        I was reviewing businesses in your area
        and noticed an opportunity regarding
        {service.lower()}.

        I help businesses improve their websites,
        SEO and online conversions.

        I was wondering whether you'd be open
        to a complimentary assessment.

        It only takes a few minutes to explain.
        """).strip()

    # --------------------------------------------------
    # Proposal Intro
    # --------------------------------------------------

    def generate_proposal_intro(self, opportunity):

        service = (
            opportunity.primary_service
            or "website improvements"
        )

        return dedent(f"""
        Thank you for considering this proposal.

        After reviewing
        {opportunity.business_name},
        I identified opportunities related to
        {service.lower()}.

        This proposal outlines practical
        recommendations that can improve your
        online presence, strengthen customer
        engagement and support future growth.
        """).strip()