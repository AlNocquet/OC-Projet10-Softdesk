"""
Core models for SoftDesk Support.

This module defines models related to application-level concerns such as
health checks and GDPR-compliant user profile management.
"""

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """
    Stores additional GDPR-related information for a user.

    This model is linked one-to-one with the Django user model and
    contains personal data fields required for GDPR compliance.

    Fields:
        user (OneToOneField): Associated user account.
        age (PositiveIntegerField): User age (must be >= 15).
        can_be_contacted (BooleanField): Consent to be contacted.
        can_data_be_shared (BooleanField): Consent to share data.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self):
        """Return a readable representation of the user profile."""
        return f"Profile of {self.user.username}"