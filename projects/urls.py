"""Routing for the project domain.

Exposes:
- /api/projects/                      -> ProjectViewSet
- /api/projects/<project_id>/issues/  -> IssueViewSet (nested)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet, ContributorViewSet, CommentViewSet


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

issue_list = IssueViewSet.as_view({"get": "list", "post": "create"})
issue_detail = IssueViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})

contributor_list = ContributorViewSet.as_view({"get": "list", "post": "create"})
contributor_detail = ContributorViewSet.as_view({"delete": "destroy"})

comment_list = CommentViewSet.as_view({"get": "list", "post": "create"})
comment_detail = CommentViewSet.as_view({
    "patch": "partial_update",
    "delete": "destroy"
})

urlpatterns = [
    path("", include(router.urls)),

    path("projects/<int:project_id>/contributors/", contributor_list, name="contributor-list"),
    path("projects/<int:project_id>/contributors/<int:pk>/", contributor_detail, name="contributor-detail"),

    path("projects/<int:project_id>/issues/", issue_list, name="issue-list"),
    path("projects/<int:project_id>/issues/<int:pk>/", issue_detail, name="issue-detail"),

    path("projects/<int:project_id>/issues/<int:issue_id>/comments/", comment_list, name="comment-list"),
    path("projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/", comment_detail, name="comment-detail"),
]

