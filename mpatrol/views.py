from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import constants
from .models import Game, Player
from .forms import ResumeForm, JoinForm

class ActivePlayerMixin(LoginRequiredMixin):
    def get_object(self):
        try:
            return Player.objects.get(pk=self.request.session.get('mpatrol_player_pk', None), user=self.request.user)
        except:
            self.request.session['mpatrol_player_pk'] = None
            return None
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = self.get_object()
        return context
    
    def get(self, request):
        self.object = self.get_object()
        if not self.object: #and request.path_info not in [reverse_lazy('mpatrol:start'), reverse_lazy('mpatrol:join')]:
            return redirect(reverse_lazy('mpatrol:index'))
        return super().get(request)

        
class IndexView(TemplateView):
    template_name = 'mpatrol/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['resume_form'] = ResumeForm(self.request.user)
            context['join_form'] = JoinForm(self.request.user)
        return context


class HomeView(ActivePlayerMixin, TemplateView):
    template_name = 'mpatrol/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        context['calc'] = context['player'].calc()
        return context
        
    def get(self, request):
        return super().get(request)
        

class ReferenceView(ActivePlayerMixin, TemplateView):
    template_name = 'mpatrol/reference.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['constants'] = constants
        return context
    
    
class ResumeFormView(LoginRequiredMixin,FormView):
    template_name = 'mpatrol/resume.html'
    form_class = ResumeForm
    success_url = reverse_lazy('mpatrol:home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        
    def form_valid(self, form):
        self.request.session['mpatrol_player_pk'] = form.cleaned_data['player'].pk
        return super().form_valid(form)
        

class JoinFormView(LoginRequiredMixin, FormView):
    template_name = 'mpatrol/join.html'
    form_class = JoinForm
    success_url = reverse_lazy('mpatrol:home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        
    def form_valid(self, form):
        p = Player(game=form.cleaned_data['game'], user=self.request.user, character_name=form.cleaned_data['character_name'])
        p.save()
        for i in range(1,9):
            p.battalion_set.create(battalion_number=i)
        p.save()
        self.request.session['mpatrol_player_pk'] = p.pk
        return super().form_valid(form)
