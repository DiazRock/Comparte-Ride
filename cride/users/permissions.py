""" User permission """

# Django REST framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """ Access only to objects owned by the requesting user """
    
    def has_object_permission(self, request, view, obj):
        """ Check obj and user are the same. """
        
        return request.user == obj