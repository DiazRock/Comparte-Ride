""" Circle views """

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated


# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


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
    
    # Filters
    filter_backend = (SearchFilter, OrderingFilter, DjangoFilterBackend) 
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offerted', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ('-members__count', '-rides_offerted', '-rides_taken')
    filter_fields = ('verified', 'is_limited')
    
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
    