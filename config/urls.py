"""Project-level URL configuration for SoftDesk Support.

Routes:
- /admin/                      -> Django admin
- /api/auth/token/             -> obtain JWT (POST)
- /api/auth/token/refresh/     -> refresh access token (POST)
- /health/                     -> includes core health & ping endpoints
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("health/", include("core.urls")),
]