from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import models
from . import serializers
from rest_framework import generics, permissions
import itertools

#@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'timetracker/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_entries = models.Entry.objects.filter(user=self.request.user)
            context['open_entries'] = user_entries.filter(end=None)
            context['recent_entries'] = user_entries.exclude(end=None)[:3]
        return context
    
    
class EntryListCreate(generics.ListCreateAPIView):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    
    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(user=self.request.user)
        
        
class RecentEntryList(generics.ListAPIView):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    
    def get_queryset(self):
        q = super().get_queryset().filter(user=self.request.user)
        q = itertools.chain(q.filter(end=None),q.exclude(end=None)[:3])
        return q