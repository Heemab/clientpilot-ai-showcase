from django.conf import settings
from django.db import models
from django.utils import timezone


class Lead(models.Model):

    STATUS_CHOICES = [
        ("new", "New"),
        ("qualified", "Qualified"),
        ("won", "Won"),
        ("lost", "Lost"),
    ]

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="leads",
    )

    company_name = models.CharField(max_length=255)

    contact_name = models.CharField(
        max_length=255,
        blank=True,
    )

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    website = models.URLField(blank=True)

    address = models.TextField(blank=True)

    category = models.CharField(
        max_length=255,
        blank=True,
    )

    source = models.CharField(
        max_length=100,
        default="Google Maps",
    )

    rating = models.FloatField(default=0)

    reviews = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    notes = models.TextField(blank=True)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.company_name


class LeadTask(models.Model):
    """
    CRM task associated with a lead.

    This model also serves as the foundation for:
    - Calendar
    - Follow-up Scheduler
    - Notifications
    - AI Copilot
    """

    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_TODO, "To Do"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_URGENT = "urgent"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_URGENT, "Urgent"),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lead_tasks",
    )

    completed_at = models.DateTimeField(
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
        ordering = [
            "status",
            "-priority",
            "due_date",
            "-created_at",
        ]

    def __str__(self):
        return f"{self.lead.company_name} - {self.title}"

    @property
    def is_overdue(self):
        return (
            self.due_date
            and self.status != self.STATUS_COMPLETED
            and self.due_date < timezone.now()
        )

    def mark_completed(self):
        self.status = self.STATUS_COMPLETED
        self.completed_at = timezone.now()
        self.save(
            update_fields=[
                "status",
                "completed_at",
                "updated_at",
            ]
        )