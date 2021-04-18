""" Circle views """

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership

# Permissions
from cride.circles.permissions import IsCircleAdmin 


class CircleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    """ Circle viewset """

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'
    
    
    def get_queryset(self):
        """ Restrict list to public-only """
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public = True)
        return queryset

    def get_permissions(self):
        """ Assign permission based on action """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [p() for p in permissions]

    def perform_create(self, serializer):
        """ Assign circle admin """
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user = user,
            profile = profile,
            circle= circle,
            is_admin= True,
            remaining_invitations= 10
        )
    