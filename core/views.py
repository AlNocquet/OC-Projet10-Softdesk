"""Core views for SoftDesk Support.

Exposes:
- HealthView: public health-check endpoint used to verify that the API is up.
- ProtectedPingView: JWT-protected sanity-check endpoint to verify authentication.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


class HealthView(APIView):
    """Public health-check endpoint.

    Returns a minimal JSON payload that allows tooling (or humans) to confirm the
    API server is running without requiring authentication.

    Permissions:
        AllowAny – this is the only public endpoint on purpose.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """Return a simple JSON status payload."""
        return Response({"status": "ok", "app": "softdesk"})


class ProtectedPingView(APIView):
    """JWT-protected ping endpoint.

    Useful during development and smoke tests to ensure that authentication is
    correctly enforced and the current user is properly resolved by DRF.

    Permissions:
        IsAuthenticated – requires a valid Bearer token (JWT access token).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return a short JSON message along with the current username."""
        return Response({"message": "pong", "user": request.user.username})