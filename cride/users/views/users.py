""" Users views """

# Django REST Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# Serializers
from cride.users.serializers import UserLoginSerializer, UserModelSerializer


class UserLoginAPIView(APIView):
    """ User Login Api View """
    
    def post(self, request, *args, **kwargs):
        """ Handle HTTP POST request """
        serializer = UserLoginSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status = status.HTTP_201_CREATED)

class UserLoginAPIView(APIView):
    """ User sign up API View """
    
    def post(self, request, *args, **kwargs):
        """ Handle HTTP POST request """
        serializer = UserSignUpView(data= request.data)
        serializer.is_valid(raise_exception= True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status = status.HTTP_201_CREATED)
        
    