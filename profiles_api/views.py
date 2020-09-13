from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class HelloApiView(APIView):
    """Test API View"""
    def get(self, request, format=None):
        """Returns a list of API view features"""
        an_apiview = [
             'Uses HTTP methods as functions(get, post, patch, put, delete)',
             'Is similar to traditional Django view',
             'Give you the most control over your app logic',
             'Is mapped manually to URLs'
         ]
        return Response({'message':'Hello!', 'an_apiview':an_apiview})