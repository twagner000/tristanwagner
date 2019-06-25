from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

import itertools

from . import models
from . import serializers

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user        


class IndexView(TemplateView):
    template_name = 'timetracker/index.html'
    
    
class EntryViewSet(viewsets.ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    #permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(owner=self.request.user)
        
    @action(detail=False)
    def recent(self, request):
        q = self.get_queryset()
        q = itertools.chain(q.filter(end=None),q.exclude(end=None)[:3])
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    '''def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [permissions.IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]'''
        
class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.BriefTaskSerializer
    permission_classes = [permissions.AllowAny]
    
