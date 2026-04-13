"""URL patterns for the core app.

This module exposes:
- /health/         -> public health check (no auth)
- /health/ping/    -> protected ping (requires JWT)
- /profile/        -> authenticated user profile (GET, PATCH, DELETE)
"""

from django.urls import path
from .views import HealthView, ProtectedPingView, UserProfileView

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
    path("ping/", ProtectedPingView.as_view(), name="protected-ping"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]