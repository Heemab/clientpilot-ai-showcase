from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.organizations.models import Organization


class User(AbstractUser):
    """
    Custom user model for the AI Client Acquisition Engine.
    """

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    job_title = models.CharField(
        max_length=100,
        blank=True,
    )

    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.username