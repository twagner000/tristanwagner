from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Creature


class IndexView(TemplateView):
    template_name = 'mpatrol/index.html'
    
class CreatureListView(ListView):
    model = Creature
