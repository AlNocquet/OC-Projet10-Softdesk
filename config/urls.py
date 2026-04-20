"""Project-level URL configuration for SoftDesk Support."""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import HealthView, ProtectedPingView

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT authentication
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Technical endpoints
    path("health/", HealthView.as_view(), name="health"),
    path("health/ping/", ProtectedPingView.as_view(), name="protected-ping"),

    # Business API
    path("api/", include("projects.urls")),
    path("api/", include("core.urls")),
]