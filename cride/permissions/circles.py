""" Circles permission classes """

# Django REST framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership

class IsCircleAdmin(BasePermission):
    """ Allow  access only to circle admins."""
    
    def has_object_permission(self, request, view, obj):
        """ Verify user have membership in the obj """
        try:
            Membership.objects.get(
                user = request.user,
                circle = obj,
                is_admin= True,
                is_active= True
            )
        except Membership.DoesNotExists:
            return False
        return True
            
