"""Routing for the project domain.

Exposes:
- /api/projects/                      -> ProjectViewSet
- /api/projects/<project_id>/issues/  -> IssueViewSet (nested)
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

issue_list = IssueViewSet.as_view({"get": "list", "post": "create"})
issue_detail = IssueViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})

urlpatterns = [
    path("", include(router.urls)),
    path("projects/<int:project_id>/issues/", issue_list, name="issue-list"),
    path("projects/<int:project_id>/issues/<int:pk>/", issue_detail, name="issue-detail"),
]