from django.db import models

from apps.leads.models import Lead
from apps.audits.models import Audit


class Proposal(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    proposal_number = models.CharField(
        max_length=30,
        unique=True,
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="proposals",
    )

    audit = models.OneToOneField(
        Audit,
        on_delete=models.CASCADE,
        related_name="proposal",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    version = models.PositiveIntegerField(
        default=1,
    )

    executive_summary = models.TextField(
        blank=True,
    )

    estimated_hours = models.PositiveIntegerField(
        default=0,
    )

    estimated_timeline = models.CharField(
        max_length=100,
        blank=True,
    )

    estimated_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    terms = models.TextField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.proposal_number