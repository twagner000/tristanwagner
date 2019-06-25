from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import generics, viewsets, views, mixins, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class AuthTokenViewSet(viewsets.ViewSet):
    authentication_classes = (authentication.SessionAuthentication,)
    
    def list(self, request, format=None):
        token, created = Token.objects.get_or_create(user=self.request.user)
        return Response({'token': token.key})
        
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}) 
        return Response()
        
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
