from rest_framework import permissions
from django.utils.translation import gettext_lazy as _

class IsUserAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.role == 1:
            return False
        else:
            return True
        