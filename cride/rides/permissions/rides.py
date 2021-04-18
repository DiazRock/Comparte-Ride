""" Rides permissions """

# Django REST framework
from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):
    """ Verify requesting user is the ride create. """
    
    def has_object_permission(self, request, view, obj):
        """ Verify requesting user is the ride creator """
        return request.user == obj.offerted_by
    
class IsNotRideOwner(BasePermission):
    """Verify the passenger is not owner of ride"""

    def has_object_permission(self, request, view, obj):
        """check request user doesn't equal to object"""
        return request.user != obj.offerted_by
        