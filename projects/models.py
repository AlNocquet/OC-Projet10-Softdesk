"""Domain models for SoftDesk Support.

This module defines the core business entities required by the bug-tracking API.
We keep field definitions intentionally minimal at this stage; the next step will
add concrete fields, relations, constraints and choices as per the specs:
- Project with author and created_time
- Contributor linking a user to a project
- Issue with priority/tag/status, assignee, author, created_time
- Comment with UUID, description, author, created_time
"""

from __future__ import annotations

import uuid
from django.conf import settings
from django.db import models


class Project(models.Model):
    """A software project that groups issues and contributors.

    Notes
    -----
    - Contains: name, description, type (backend/frontend/iOS/Android),
      author (FK to user), created_time (auto timestamp).
    - Only contributors of a project can read its details; only the author can
      update/delete it (authorization rules enforced at the view/permission layer).
    """

    class Type(models.TextChoices):
        BACK_END = "BACK_END", "Back-end"
        FRONT_END = "FRONT_END", "Front-end"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=16, choices=Type.choices)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_projects",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Contributor(models.Model):
    """Membership link between a user and a project.

    Notes
    -----
    - Contains: user (FK to AUTH_USER_MODEL), project (FK to Project),
      optional role if needed later (e.g., author/maintainer).
    - Used by permissions to restrict visibility and actions to project members.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="contributors",
    )

    def __str__(self) -> str:
        return f"{self.user} -> {self.project.name}"

    class Meta:
        verbose_name = "Contributor"
        verbose_name_plural = "Contributors"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"], name="uniq_contributor_per_project"
            )
        ]


class Issue(models.Model):
    """A ticket (bug/feature/task) tracked within a project.

    Notes
    -----
    - Contains: title, description, priority (LOW/MEDIUM/HIGH),
      tag (BUG/FEATURE/TASK), status (TO_DO/IN_PROGRESS/FINISHED),
      assignee (FK to user, must be a contributor of the same project),
      project (FK), author (FK), created_time (auto timestamp).
    - Only the author can update/delete; all project contributors can read.
    """

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class Tag(models.TextChoices):
        BUG = "BUG", "Bug"
        FEATURE = "FEATURE", "Feature"
        TASK = "TASK", "Task"

    class Status(models.TextChoices):
        TO_DO = "TO_DO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        FINISHED = "FINISHED", "Finished"

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=8, choices=Priority.choices, default=Priority.MEDIUM)
    tag = models.CharField(max_length=8, choices=Tag.choices, default=Tag.BUG)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.TO_DO)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_issues",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
        help_text="Must be a contributor of the same project (validated at the API layer).",
    )

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.tag}/{self.priority}] {self.title}"

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Issue"
        verbose_name_plural = "Issues"



class Comment(models.Model):
    """A comment posted on an issue to discuss or clarify it.

    Notes
    -----
    - Contains: uuid (auto), description (text), issue (FK),
      author (FK to user), created_time (auto timestamp).
    - Visible to project contributors; update/delete restricted to the author.
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment {self.uuid} on #{self.issue_id}"

    class Meta:
        ordering = ["created_time"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"