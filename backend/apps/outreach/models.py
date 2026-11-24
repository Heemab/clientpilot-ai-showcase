from django.conf import settings
from django.db import models

from apps.proposals.models import Proposal


class Outreach(models.Model):

    STATUS_DRAFT = "draft"
    STATUS_READY = "ready"
    STATUS_SENT = "sent"
    STATUS_OPENED = "opened"
    STATUS_REPLIED = "replied"
    STATUS_MEETING = "meeting"
    STATUS_WON = "won"
    STATUS_LOST = "lost"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_READY, "Ready"),
        (STATUS_SENT, "Sent"),
        (STATUS_OPENED, "Opened"),
        (STATUS_REPLIED, "Replied"),
        (STATUS_MEETING, "Meeting Booked"),
        (STATUS_WON, "Won"),
        (STATUS_LOST, "Lost"),
    ]

    proposal = models.OneToOneField(
        Proposal,
        on_delete=models.CASCADE,
        related_name="outreach",
    )

    subject = models.CharField(max_length=255)

    cold_email = models.TextField()

    follow_up_1 = models.TextField()

    follow_up_2 = models.TextField()

    linkedin_message = models.TextField()

    whatsapp_message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.proposal.lead.company_name} ({self.get_status_display()})"


class OutreachEvent(models.Model):
    """
    CRM timeline/history for an outreach.
    """

    EVENT_GENERATED = "generated"
    EVENT_DRAFT_SAVED = "draft_saved"
    EVENT_EMAIL_SENT = "email_sent"
    EVENT_FOLLOWUP_1_SENT = "followup_1_sent"
    EVENT_FOLLOWUP_2_SENT = "followup_2_sent"
    EVENT_OPENED = "opened"
    EVENT_REPLIED = "replied"
    EVENT_MEETING = "meeting"
    EVENT_WON = "won"
    EVENT_LOST = "lost"

    EVENT_CHOICES = [
        (EVENT_GENERATED, "Outreach Generated"),
        (EVENT_DRAFT_SAVED, "Draft Saved"),
        (EVENT_EMAIL_SENT, "Cold Email Sent"),
        (EVENT_FOLLOWUP_1_SENT, "Follow-up #1 Sent"),
        (EVENT_FOLLOWUP_2_SENT, "Follow-up #2 Sent"),
        (EVENT_OPENED, "Email Opened"),
        (EVENT_REPLIED, "Lead Replied"),
        (EVENT_MEETING, "Meeting Scheduled"),
        (EVENT_WON, "Client Won"),
        (EVENT_LOST, "Client Lost"),
    ]

    outreach = models.ForeignKey(
        Outreach,
        on_delete=models.CASCADE,
        related_name="events",
    )

    event_type = models.CharField(
        max_length=30,
        choices=EVENT_CHOICES,
    )

    notes = models.TextField(
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.get_event_type_display()} - "
            f"{self.outreach.proposal.lead.company_name}"
        )