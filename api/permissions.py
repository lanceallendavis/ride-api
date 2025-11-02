from rest_framework.permissions import BasePermission

from .models import RideUser

class IsRideAdmin(BasePermission):
    """
    - Checks role that allows access to endpoints for Admins only.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            
            return False
        
        return request.user.role == RideUser.RoleChoices.ADMIN