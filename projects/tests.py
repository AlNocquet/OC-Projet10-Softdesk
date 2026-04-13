from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, Contributor, Issue, Comment


User = get_user_model()


class ProjectContributorIssueCommentTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="Alice",
            password="admin0777"
        )
        self.olivier = User.objects.create_user(
            username="Olivier",
            password="admin0777"
        )
        self.test3 = User.objects.create_user(
            username="Test_3",
            password="admin0777"
        )

        self.client.force_authenticate(user=self.alice)

        self.project = Project.objects.create(
            name="Projet test",
            description="Projet de test",
            type="BACK_END",
            author=self.alice,
        )
        Contributor.objects.create(user=self.alice, project=self.project)

    def test_project_author_is_auto_added_as_contributor_on_create(self):
        payload = {
            "name": "Projet auto contributor",
            "description": "Test auto-add",
            "type": "BACK_END",
        }

        response = self.client.post("/api/projects/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project_id = response.data["id"]

        self.assertTrue(
            Contributor.objects.filter(
                user=self.alice,
                project_id=project_id
            ).exists()
        )

    def test_only_project_author_can_add_contributor(self):
        Contributor.objects.create(user=self.olivier, project=self.project)

        self.client.force_authenticate(user=self.olivier)

        payload = {"user": "Test_3"}
        response = self.client.post(
            f"/api/projects/{self.project.id}/contributors/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_author_can_add_contributor(self):
        payload = {"user": "Olivier"}

        response = self.client.post(
            f"/api/projects/{self.project.id}/contributors/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Contributor.objects.filter(
                user=self.olivier,
                project=self.project
            ).exists()
        )

    def test_duplicate_contributor_is_rejected(self):
        Contributor.objects.create(user=self.olivier, project=self.project)

        payload = {"user": "Olivier"}

        response = self.client.post(
            f"/api/projects/{self.project.id}/contributors/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user", response.data)

    def test_issue_assignee_must_be_project_contributor(self):
        payload = {
            "title": "Issue test",
            "description": "Description",
            "priority": "HIGH",
            "tag": "BUG",
            "status": "TO_DO",
            "assignee": "Olivier",
        }

        response = self.client.post(
            f"/api/projects/{self.project.id}/issues/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("assignee", response.data)

    def test_comment_author_only_can_update_comment(self):
        Contributor.objects.create(user=self.olivier, project=self.project)

        issue = Issue.objects.create(
            title="Issue 1",
            description="Issue desc",
            priority="MEDIUM",
            tag="TASK",
            status="TO_DO",
            project=self.project,
            author=self.alice,
        )

        comment = Comment.objects.create(
            description="Commentaire initial",
            issue=issue,
            author=self.alice,
        )

        self.client.force_authenticate(user=self.olivier)

        response = self.client.patch(
            f"/api/projects/{self.project.id}/issues/{issue.id}/comments/{comment.id}/",
            {"description": "Hack"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)