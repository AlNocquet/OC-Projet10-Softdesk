"""
Core serializers for SoftDesk Support.

This module defines serializers used to handle user profile data
in compliance with GDPR requirements.
"""

from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    Provides read and write access to GDPR-related user data.
    The associated username is exposed as a read-only field.

    Validation:
        - Age must be at least 15 years old.
    """

    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    def validate_age(self, value):
        """
        Ensure that the user meets the minimum legal age requirement.

        Args:
            value (int): Age provided in the request.

        Returns:
            int: Validated age.

        Raises:
            ValidationError: If age is below 15.
        """
        if value < 15:
            raise serializers.ValidationError(
                "User must be at least 15 years old to give consent."
            )
        return value