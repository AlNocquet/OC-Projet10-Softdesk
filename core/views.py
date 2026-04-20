"""Views for the core app.

This module exposes:
- a public health-check endpoint
- a JWT-protected ping endpoint
- a public sign-up endpoint that creates both User and UserProfile
- an authenticated GDPR profile endpoint for read, update, and delete

Routing intent
--------------
- technical endpoints stay outside the business domain
- registration collects GDPR data explicitly at account creation time
- profile management is restricted to the authenticated user's own profile
"""

from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import SignUpSerializer, UserProfileSerializer


class HealthView(APIView):
    """Public health-check endpoint.

    This endpoint is meant for smoke tests and quick server availability checks.
    It does not require authentication.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """Return a minimal payload confirming that the API is running."""
        return Response({"status": "ok", "app": "softdesk"})


class ProtectedPingView(APIView):
    """JWT-protected ping endpoint.

    This endpoint is useful to verify that:
    - JWT authentication works
    - the authenticated user is correctly resolved as `request.user`
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return a short authenticated response with the current username."""
        return Response({"message": "pong", "user": request.user.username})


class SignUpView(generics.CreateAPIView):
    """Public registration endpoint with explicit GDPR data collection.

    Expected input:
    - username
    - password
    - age
    - can_be_contacted
    - can_data_be_shared

    Created objects:
    - Django User
    - related UserProfile
    """

    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Create the account and return a simplified success payload."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User created successfully.",
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Authenticated GDPR profile endpoint.

    Allowed operations:
    - GET: access the authenticated user's personal GDPR data
    - PATCH/PUT: rectify personal GDPR data
    - DELETE: right to be forgotten (delete the account)

    Important:
    - the profile must already exist because it is created at sign-up time
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the profile associated with the authenticated user.

        Raises:
            Http404: If the profile does not exist.
        """
        return get_object_or_404(UserProfile, user=self.request.user)

    def perform_destroy(self, instance):
        """Delete the authenticated user's account.

        The related profile is automatically deleted by cascade because the
        profile is linked to the user with a OneToOneField using CASCADE.
        """
        self.request.user.delete()
