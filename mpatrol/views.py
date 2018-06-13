from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from . import constants
from .models import Player


class IndexView(TemplateView):
    template_name = 'mpatrol/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        if self.request.user.is_authenticated():
            p = Player.objects.filter(user=self.request.user, game__ended_date__isnull=True)        
            if len(p) == 1:
                context['player'] = p[0]
                context['calc'] = p[0].calc()
        return context
    
class ReferenceView(TemplateView):
    template_name = 'mpatrol/reference.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        return context
    