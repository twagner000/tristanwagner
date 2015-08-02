from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from .models import Game, Turn
from .forms import GameForm, CropsForm, BudgetForm, DebtForm, EndTurnForm
import math
import random

class CurrentTurnMixin(object):
    success_url = reverse_lazy('deveconsim:index')
    
    def open_games(self):
        g = Game.objects.filter(pk=self.request.session.get('deveconsim_game_pk', None), completed_date__isnull=True)
        if self.request.user.is_authenticated():
            g = g | Game.objects.filter(user=self.request.user, completed_date__isnull=True)
        return g
    
    def get_object(self):
        g = self.open_games()
        if len(g) == 1:
            return g[0].last_turn()
    
    def get_context_data(self, **kwargs):
        context = super(CurrentTurnMixin, self).get_context_data(**kwargs)
        if context.get('turn'):
            context['calc'] = context['turn'].calc()
        context['open_games'] = self.open_games()
        return context
    
    def get(self, request):
        self.object = self.get_object()
        if not self.object and request.path_info != reverse_lazy('deveconsim:start'):
            return redirect(reverse_lazy('deveconsim:start'))
        return super(CurrentTurnMixin, self).get(request)

class GameFormView(CurrentTurnMixin,FormView):
    template_name = 'deveconsim/game_form.html'
    form_class = GameForm
    success_url = reverse_lazy('deveconsim:index')
    
    def get_form_kwargs(self):
        kwargs = super(GameFormView, self).get_form_kwargs()
        kwargs.update({'open_games' : self.open_games().order_by('-started_date')})
        return kwargs
        
    def form_valid(self, form):
        pk = form['continue_game'].value()
        pk = pk if pk else None
        keep = Game.objects.filter(pk=pk, completed_date__isnull=True)
        if len(keep) == 1:
            keep = keep[0]
        else:
            keep = Game(name=form['name'].value())
            if self.request.user.is_authenticated():
                keep.user = self.request.user
            keep.save()
            keep.turn_set.create()
            keep.save()
        self.request.session['deveconsim_game_pk'] = keep.pk
        for game in self.open_games():
            if game != keep:
                game.completed_date = timezone.now()
                if self.request.user.is_authenticated():
                    game.user = self.request.user
                game.save()
        return super(GameFormView, self).form_valid(form)
                
class TurnDetailView(CurrentTurnMixin, DetailView):
    pass
        
class CropsUpdateView(CurrentTurnMixin, UpdateView):
    form_class = CropsForm
    template_name_suffix = '_crops_form'
    
class BudgetUpdateView(CurrentTurnMixin, UpdateView):
    form_class = BudgetForm
    template_name_suffix = '_budget_form'
            
class DebtUpdateView(CurrentTurnMixin, UpdateView):
    form_class = DebtForm
    template_name_suffix = '_debt_form'
    
class EndTurnUpdateView(CurrentTurnMixin, UpdateView):
    form_class = EndTurnForm
    
    def form_valid(self, form):
        turn = self.object
        calc = turn.calc()
        turn.completed_date = timezone.now()
        
        #check for voted out
        if calc['hap_lgen'] <= .3 and random.random() <= 1.1559*math.exp(-7.41*calc['hap_lgen']) and turn.turn > 3:
            turn.voted_out = True
            turn.save()
            turn.game.completed_date = turn.completed_date
            turn.game.save()
            return redirect('deveconsim:voted_out', pk=turn.game.pk)
        else:
            turn.save()
            turn.pk = None
            turn.genfund = calc['new_genfund']+turn.debt_new_wbsap-calc['wbsap_add_cocoa_cost']
            turn.cocoa += turn.wbsap_cocoa
            turn.wbsap_cocoa = 0
            turn.start_corn = turn.corn
            turn.start_cocoa = turn.cocoa
            if turn.debt_new_wbsap and turn.svc_health > 15:
                turn.svc_health = 15
            if turn.debt_new_wbsap and turn.svc_security > 20:
                turn.svc_security = 20
            
            #check for decapitalization AFTER SAP cocoa planted in case auto-readjust crops
            turn.decapitalized = False
            if calc['hap_ugen'] <= .3 and random.random() <= 1.1559*math.exp(-7.41*calc['hap_ugen']) and turn.turn > 3 and turn.land >= 100:
                turn.land -= 100
                turn.decapitalized = True
            
            #update turn AFTER vote/decap tutorial checks
            turn.turn += 1
            
            turn.debt_private -= turn.debt_repay_private
            turn.debt_wb -= turn.debt_repay_wb
            turn.debt_wbsap += turn.debt_new_wbsap-turn.debt_repay_wbsap
            turn.debt_repay_private = 0
            turn.debt_repay_wb = 0
            turn.debt_repay_wbsap = 0
            turn.debt_new_wbsap = 0
            turn.landprod *= (1-turn.game.PESTICIDES[turn.pesticides]['prod_loss'])
            turn.save()
        return super(EndTurnUpdateView, self).form_valid(form)

class VotedOutView(DetailView):
    model = Game
    template_name = 'deveconsim/game_voted_out.html'
    
    def get(self, request, pk):
        self.object = self.get_object()
        if self.object.pk != self.request.session.get('deveconsim_game_pk', None):
            if self.request.user.is_authenticated() and self.object.user != self.request.user:
                return redirect(reverse_lazy('deveconsim:start'))
        return super(VotedOutView, self).get(request)
