from django.db import models


class Audit(models.Model):

    lead = models.ForeignKey(
        "leads.Lead",
        on_delete=models.CASCADE,
        related_name="audits",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # ------------------------------------------------------------------
    # Website Information
    # ------------------------------------------------------------------

    website = models.URLField()

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------

    ssl_enabled = models.BooleanField(default=False)

    https_redirect = models.BooleanField(default=False)

    # ------------------------------------------------------------------
    # SEO
    # ------------------------------------------------------------------

    page_title = models.CharField(
        max_length=255,
        blank=True,
    )

    meta_description = models.TextField(
        blank=True,
    )

    h1_count = models.PositiveIntegerField(default=0)

    h2_count = models.PositiveIntegerField(default=0)

    image_count = models.PositiveIntegerField(default=0)

    missing_alt_count = models.PositiveIntegerField(default=0)

    canonical_url = models.URLField(
        blank=True,
        default="",
    )

    has_viewport = models.BooleanField(default=False)

    has_open_graph = models.BooleanField(default=False)

    has_twitter_card = models.BooleanField(default=False)

    html_lang = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    has_favicon = models.BooleanField(default=False)

    # ------------------------------------------------------------------
    # Technology
    # ------------------------------------------------------------------

    cms = models.CharField(
        max_length=100,
        blank=True,
        default="Unknown",
    )

    theme = models.CharField(
        max_length=100,
        blank=True,
        default="Unknown",
    )

    technologies = models.JSONField(
        default=list,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Performance
    # ------------------------------------------------------------------

    load_time = models.FloatField(default=0)

    performance_score = models.PositiveIntegerField(default=0)

    # ------------------------------------------------------------------
    # Mobile
    # ------------------------------------------------------------------

    mobile_friendly = models.BooleanField(default=False)

    # ------------------------------------------------------------------
    # Accessibility
    # ------------------------------------------------------------------

    accessibility_score = models.PositiveIntegerField(default=0)

    # ------------------------------------------------------------------
    # Scores
    # ------------------------------------------------------------------

    seo_score = models.PositiveIntegerField(default=0)

    overall_score = models.PositiveIntegerField(default=0)

    # ------------------------------------------------------------------
    # AI Recommendations
    # ------------------------------------------------------------------

    executive_summary = models.TextField(
        blank=True,
        default="",
    )

    critical_issues = models.JSONField(
        default=list,
        blank=True,
    )

    high_priority = models.JSONField(
        default=list,
        blank=True,
    )

    medium_priority = models.JSONField(
        default=list,
        blank=True,
    )

    good_practices = models.JSONField(
        default=list,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Business Opportunities
    # ------------------------------------------------------------------

    opportunities = models.JSONField(
        default=list,
        blank=True,
    )

    estimated_project_hours = models.PositiveIntegerField(
        default=0,
    )

    estimated_project_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # ------------------------------------------------------------------
    # Raw Results
    # ------------------------------------------------------------------

    raw_results = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.lead.company_name} Audit "
            f"({self.created_at:%Y-%m-%d %H:%M})"
        )