from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# Create your views here.

class HelloApiView(APIView):
    """Tests API View"""

    serializer_class=serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of API view features"""
        an_apiview = [
             'Uses HTTP methods as functions(get, post, patch, put, delete)',
             'Is similar to traditional Django view',
             'Give you the most control over your app logic',
             'Is mapped manually to URLs'
         ]
        return Response({'message':'Hello!', 'an_apiview':an_apiview})
    
    def post(self, request): # not possible without serializer
        """Create a hello message with our name"""

        serializer = self.serializer_class(data = request.data)

        # Validation
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}' 
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None): #pk of id of objects to be updated (DB)
        """Handles updating an object"""
        return Response({'method':'PUT'})
    
    def patch(self, request, pk=None): #pk of id of objects to be updated (DB)
        """Handles partial updating an object"""
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None): #pk of id of objects to be updated (DB)
        """Deletes an object"""
        return Response({'method':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, ) #tuple

    permission_classes = (permissions.UpdateOwnProfile, )

    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken): #for unsafe methods
    """Handles creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES #viewsets has this by def but not here


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    "Handles creating reading and updating profile feed items"
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    permission_classes = (permissions.UpdateOwnStatus,
    IsAuthenticated)

    def perform_create(self, serializer):
        print("hello", self.request.user)
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)