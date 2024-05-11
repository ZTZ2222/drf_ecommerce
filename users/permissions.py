from rest_framework.permissions import BasePermission


class IsUserAddressOwner(BasePermission):
    """
    Check if authenticated user is owner of the address
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
