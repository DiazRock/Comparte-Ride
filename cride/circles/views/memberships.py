""" Circle membership views """

# Django REST framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404 


# Serializers
from cride.circles.serializers import MembershipModelSerializer


# Models
from cride.circles.models import Circle, Membership


class MemberShipViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """ Circle membership viewset """
    
    serializer_class = MembershipModelSerializer
        
    def get_queryset(self):
        """ Return circle members """
        return Membership.objects.filter (
            circle = self.circle,
            is_active = True
        )
    
    def dispatch(self, request, *args, **kwargs):
        """ Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name= slug_name)
        return super(MemberShipViewSet, self).dispatch(request, *args, **kwargs)
    
    