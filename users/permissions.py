from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Custom permission to allow "les personnels adminstratifs" to create accounts
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type in ["superuser", "admin"]
