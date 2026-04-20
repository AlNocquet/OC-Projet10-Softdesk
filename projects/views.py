"""ViewSets for the project domain: projects, contributors, issues and comments."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue, Contributor, Comment
from .serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD for projects.

    Visibility:
    - Authenticated users only.
    - Users can only see projects where they are contributors.

    Write permissions:
    - Only the project author can update or delete a project.
    """

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Limit to projects where the current user is a contributor."""

        user = self.request.user
        return (
            Project.objects.filter(contributors__user=user)
            .select_related("author")
            .prefetch_related("contributors")
            .order_by("-created_time")
        )


class IssueViewSet(viewsets.ModelViewSet):
    """
    CRUD for issues nested under a project.

    Visibility:
    - Only contributors of the parent project can access its issues.

    Write permissions:
    - Only the issue author can update or delete an issue.
    """
    
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = IssueSerializer

    def _get_project(self) -> Project:
        """Fetch the project from URL kwargs and verify membership."""

        return get_object_or_404(
            Project.objects.filter(contributors__user=self.request.user),
            pk=self.kwargs["project_id"],
        )

    def get_queryset(self):
        """Limit issues to the current project."""

        project = self._get_project()
        return (
            Issue.objects.filter(project=project)
            .select_related("author", "project")
            .order_by("-created_time")
        )

    def get_serializer_context(self):
        """Inject the current project into the serializer context."""

        ctx = super().get_serializer_context()
        ctx["project"] = self._get_project()
        return ctx


class ContributorViewSet(viewsets.ModelViewSet):
    """
    Manage contributors of a project.

    Visibility:
    - Only contributors of the project can access this endpoint.

    Write permissions:
    - Only the project author can add or remove contributors.
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def _get_project(self):
        """
        Get the project only if the current user is a contributor of it.
        This prevents access to projects the user does not belong to.
        """
        return get_object_or_404(
            Project.objects.filter(contributors__user=self.request.user),
            pk=self.kwargs["project_id"],
        )

    def get_queryset(self):
        """
        List contributors of the current project.
        """
        project = self._get_project()
        return (
            Contributor.objects.filter(project=project)
            .select_related("user", "project")
            .order_by("id")
        )

    def get_serializer_context(self):
        """
        Pass the current project into the serializer.
        """
        context = super().get_serializer_context()
        context["project"] = self._get_project()
        return context

    def perform_create(self, serializer):
        """
        Only the project author can add contributors.
        """
        project = self._get_project()
        if project.author_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only the project author can add contributors.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """
        Only the project author can remove contributors.
        """
        project = self._get_project()
        if project.author_id != request.user.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only the project author can remove contributors.")
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments nested under an issue.

    Visibility:
    - Only contributors of the parent project can access its comments.

    Write permissions:
    - Only the comment author can update or delete a comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def _get_issue(self):
        """Fetch the issue from the URL and ensure the current user belongs to its project."""
        return get_object_or_404(
            Issue.objects.filter(project__contributors__user=self.request.user),
            pk=self.kwargs["issue_id"]
        )

    def get_queryset(self):
        """Return comments attached to the current issue only."""
        issue = self._get_issue()
        return Comment.objects.filter(issue=issue)

    def get_serializer_context(self):
        """Inject the current issue into the serializer context."""
        context = super().get_serializer_context()
        context["issue"] = self._get_issue()
        return context