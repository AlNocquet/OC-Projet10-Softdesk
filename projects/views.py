

"""ViewSets for the project domain (Projects and Issues)."""

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue
from .serializers import ProjectSerializer, IssueSerializer
from .permissions import IsAuthorOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD for projects.

    Visibility: only projects where the requester is a contributor.
    Write: object-level write restricted to the project author (permission).
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
    """CRUD for issues nested under a project.

    Visibility: contributors of the project only.
    Write: object-level write restricted to the issue author (permission).
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