from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import constants
from .models import Game, Player
from .forms import ResumeForm, JoinForm

class IndexView(TemplateView):
    template_name = 'mpatrol/index.html'