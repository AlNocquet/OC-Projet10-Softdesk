

"""Serializers for Projects and Issues."""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor, Issue


User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """Serialize Project instances.

    - `author` is read-only (taken from the request user).
    - On create, the creator becomes both the author AND an auto-added contributor.
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "created_time"]
        read_only_fields = ["id", "author", "created_time"]

    def create(self, validated_data):
        """Set creator as author AND auto-add as contributor."""
        user = self.context["request"].user
        project = Project.objects.create(author=user, **validated_data)
        Contributor.objects.get_or_create(user=user, project=project)
        return project


class IssueSerializer(serializers.ModelSerializer):
    """Serialize Issue instances nested under a given Project.

    Notes
    -----
    - `project` is read-only and injected from the URL (context).
    - `author` is read-only (request user).
    - `assignee` must be a contributor of the same project (validated here).
    """
    author = serializers.ReadOnlyField(source="author.username")
    assignee = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Issue
        fields = [
            "id", "title", "description",
            "priority", "tag", "status",
            "assignee", "author", "project", "created_time",
        ]
        read_only_fields = ["id", "author", "project", "created_time"]

    def validate(self, attrs):
        """Ensure the assignee (if provided) is a contributor of the project."""
        project = self.context["project"]
        assignee = attrs.get("assignee")
        if assignee and not Contributor.objects.filter(user=assignee, project=project).exists():
            raise serializers.ValidationError(
                {"assignee": "Assignee must be a contributor of this project."}
            )
        return attrs

    def create(self, validated_data):
        """Create an issue bound to the project from the URL and the request user."""
        project = self.context["project"]
        user = self.context["request"].user
        return Issue.objects.create(project=project, author=user, **validated_data)