from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'mpatrol/index.html'