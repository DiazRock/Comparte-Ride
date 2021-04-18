""" Rides serializer """

# Django REST Framework
from rest_framework import serializers


# Models
from cride.rides.models import Ride
from cride.circles.models import Membership
from cride.users.models import User

# Serializers
from cride.users.serializers import UserModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone


class CreateRideSerializer(serializers.ModelSerializer):
    """ Create ride serializer """
    
    offerted_by = serializers.HiddenField(default = serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value = 1, max_value = 15)
    
    
    class Meta:
        """ Meta class """
        model = Ride
        exclude = ('offerted_in', 'passengers', 'rating', 'is_active')

    def validate_departure_date(self, data):
        """ Verfify date is not in the past """
        min_date = timezone.now() + timedelta(minutes = 10)
        if data < min_date:
            raise serializers.ValidationError (
                'Departure time must be at least pass the next 20 minutes window'
            )
        return data
    
    def validate(self, data):
        """ Validate 
        
        Verify that the person who offers the ride is member
        and also the same user making the request
        """
        if self.context['request'].user != data['offerted_by']:
            raise serializers.ValidationError("Rides offerted on behalf of others are not allowed")
        
        user = data['offerted_by']
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(user= user, 
                                                circle= circle, 
                                                is_active= True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle')
        
        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError("Departure date must happen after arrival date")
        
        self.context['membership'] = membership
        return data
    
    def create(self, data):
        """ Create ride and update stats """
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offerted_in= circle)
        
        # Circle
        circle.rides_offerted = 1
        circle.save()
        
        # Membership
        membership= self.context['membership']
        membership.rides_offerted += 1
        membership.save()
        
        # Profile
        profile = data['offerted_by'].profile
        profile.rides_offerted += 1
        profile.save()
        
        return ride
        
        
class RideModelSerializer(serializers.ModelSerializer):
    """ Ride model serializer """
    
    offerted_by = UserModelSerializer(read_only= True)
    offerted_in = serializers.StringRelatedField()
    
    passengers = UserModelSerializer(read_only = True, many= True)
    
    class Meta:
        """ Meta class """
        model = Ride
        fields= '__all__'
        read_only_fields = (
            'offerted_by',
            'offerted_in',
            'rating'
        )

    def update(self, instance, data):
        """ Allow update only before departure date """
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('Ongoing rides cannot be modified')
        return super(RideModelSerializer, self).update(instance, data)
        
        
class JoinRideSerializer(serializers.ModelSerializer):
    """ Join Ride serializer """
    
    passenger = serializers.IntegerField()
    
    class Meta:
        """ Meta class """
        
        model= Ride
        fields = ('passenger', )
        
    def validate_passenger(self, data):
        """ Verify passenger exists and is a circle member """
        try:
            user= User.objects.get(pk = data)    
        except User.DoesNotExist :
            raise serializers.ValidationError('Invalid passenger')
        
        circle = self.context['circle']
        try:
            membership = Membership.objects.get(user= user, 
                                                circle= circle, 
                                                is_active= True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle')
        
        self.context['user'] = user
        self.context['member'] = membership
        
        return data
    
    def validate(self, data):
        """Verify rides allow new passengers."""
        ride= self.context['ride']
        if ride.departure_date <= timezone.now():
            raise serializers.ValidationError("You can't join this ride now")

        if ride.available_seats < 1:
            raise serializers.ValidationError("Ride is already full!")

        if ride.passengers.filter(pk=self.context['user'].pk).exists():
            raise serializers.ValidationError('Passenger is already in this trip')

        return data
    
    def update(self, instance, data):
        """ Add passenger to ride, and update stats """
        ride = self.context['ride']
        user = self.context['user']
        
        ride.passengers.add(user)
        
        # Profile
        profile = user.profile
        profile.rides_taken +=1 
        profile.save()
        
        # Membership
        member = self.context['member']
        member.rides_taken += 1
        
        # Circle
        circle = self.context['circle']
        circle.rides_taken += 1
        circle.save()
        
        return ride
        

class EndRideSerializer(serializers.ModelSerializer):
    """ End ride serializer """
    
    current_time = serializers.DateTimeField()
    
    class Meta:
        """ Meta class """
        
        model = Ride
        fields = ('is_active', 'current_time')
        
    def validate_current_time(self, data):
        """ Verify ride have indeed started """
        ride= self.context['view'].get_object()
        if data <= ride.departure_date:
            raise serializers.ValidationError('Ride has not started yet')
        return data


