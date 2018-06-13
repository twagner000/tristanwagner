from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from . import constants


class IndexView(TemplateView):
    template_name = 'mpatrol/index.html'
    
class ReferenceView(TemplateView):
    template_name = 'mpatrol/reference.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        return context
    