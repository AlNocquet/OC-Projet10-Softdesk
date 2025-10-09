"""URL patterns for the core app.

This module intentionally exposes:
- /health/        -> public health check (no auth)
- /health/ping/   -> protected ping (requires JWT)
"""

from django.urls import path
from .views import HealthView, ProtectedPingView

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
    path("ping/", ProtectedPingView.as_view(), name="protected-ping"),
]