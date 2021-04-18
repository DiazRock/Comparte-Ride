""" Profile Serializer """

# Django REST framework
from rest_framework import serializers


# Models
from cride.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """ Profile model serializer """
    
    
    class Meta:
        """ Meta class . """
        
        model = Profile
        fields = (
            'picture',
            'biography',
            'rides_taken',
            'rides_offerted',
            'reputation'
        )
        read_only_fields = (
            'rides_taken',
            'rides_offerted',
            'reputation'
        )
        