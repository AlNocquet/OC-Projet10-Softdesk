"""URL patterns for core user-related endpoints.

This module exposes:
- /api/signup/   -> public account creation with GDPR data
- /api/profile/  -> authenticated profile read/update/delete

Technical endpoints such as health checks and ping are intentionally routed
from the project-level URL configuration instead of being mixed here.
"""

from django.urls import path

from .views import SignUpView, UserProfileView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="sign-up"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
