

"""Custom permission classes for the project domain."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Allow read to any authenticated user; write only to the resource author.

    This is enforced at the object level. Viewsets must ensure queryset limits
    (e.g., contributors only) at the list/retrieve level.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # Works for Project/Issue/Comment as long as the model exposes `author`.
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)