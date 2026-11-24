from django.conf import settings
from django.core.mail import EmailMessage


class EmailSender:
    """
    Service responsible for sending outreach emails.
    """

    @staticmethod
    def send(outreach):
        lead = outreach.proposal.lead

        if not lead.email:
            raise ValueError(
                f"{lead.company_name} does not have an email address."
            )

        email = EmailMessage(
            subject=outreach.subject,
            body=outreach.cold_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[lead.email],
        )

        email.content_subtype = "plain"

        email.send(fail_silently=False)

        return True