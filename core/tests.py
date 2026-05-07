from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import UserProfile


User = get_user_model()


class CoreAndGdprTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Alice",
            password="admin0777"
        )

        UserProfile.objects.create(
            user=self.user,
            age=20,
            can_be_contacted=True,
            can_data_be_shared=False,
        )

    def test_health_endpoint_is_public(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")

    def test_protected_ping_requires_authentication(self):
        response = self.client.get("/health/ping/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_endpoint_returns_authenticated_user_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/profile/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "Alice")

    def test_profile_age_must_be_at_least_15(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            "/api/profile/",
            {"age": 14},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", response.data)

    def test_profile_delete_removes_user_account(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete("/api/profile/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username="Alice").exists())
