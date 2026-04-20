"""Serializers for the core app.

This module contains serializers for:
- GDPR profile read/update operations
- user sign-up with explicit GDPR data collection

Design choices
--------------
- `SignUpSerializer` creates both the Django `User` and the related `UserProfile`
  in a single request so that age and consent fields are collected at registration
  time, as required by the project specifications.
- `UserProfileSerializer` is used after registration to read and update the
  authenticated user's GDPR profile.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for GDPR-related user profile data.

    Exposes the authenticated user's GDPR profile fields and the related username.

    Read/write fields:
    - age
    - can_be_contacted
    - can_data_be_shared

    Read-only field:
    - username

    Business rule:
    - age must be at least 15.
    """

    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        """Metadata for the GDPR profile serializer."""

        model = UserProfile
        fields = [
            "username",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    def validate_age(self, value: int) -> int:
        """Ensure the legal minimum age for consent is respected.

        Args:
            value: Age sent by the client.

        Returns:
            The validated age.

        Raises:
            serializers.ValidationError: If the age is below 15.
        """
        if value < 15:
            raise serializers.ValidationError(
                "User must be at least 15 years old to give consent."
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer used to register a new user with GDPR fields.

    This serializer creates:
    - a Django `User`
    - the associated `UserProfile`

    Required registration data:
    - username
    - password
    - age
    - can_be_contacted
    - can_data_be_shared
    """

    age = serializers.IntegerField(write_only=True)
    can_be_contacted = serializers.BooleanField(write_only=True, default=False)
    can_data_be_shared = serializers.BooleanField(write_only=True, default=False)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        """Metadata for the sign-up serializer."""

        model = User
        fields = [
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    def validate_age(self, value: int) -> int:
        """Ensure the legal minimum age for consent is respected.

        Args:
            value: Age sent by the client.

        Returns:
            The validated age.

        Raises:
            serializers.ValidationError: If the age is below 15.
        """
        if value < 15:
            raise serializers.ValidationError(
                "User must be at least 15 years old to give consent."
            )
        return value

    def validate_username(self, value: str) -> str:
        """Ensure that the requested username is unique.

        Args:
            value: Username sent by the client.

        Returns:
            The validated username.

        Raises:
            serializers.ValidationError: If the username is already taken.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data: dict) -> User:
        """Create both the Django user and the related GDPR profile.

        Args:
            validated_data: Validated sign-up data.

        Returns:
            The created Django user instance.
        """
        age = validated_data.pop("age")
        can_be_contacted = validated_data.pop("can_be_contacted", False)
        can_data_be_shared = validated_data.pop("can_data_be_shared", False)
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        UserProfile.objects.create(
            user=user,
            age=age,
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared,
        )

        return user
