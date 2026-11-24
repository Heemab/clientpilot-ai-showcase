from django.db import models


class Organization(models.Model):
    """
    Company or agency using the AI Client Acquisition Engine.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)

    address = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="organizations/logos/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name