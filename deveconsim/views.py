from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from .models import Game, Turn
from .forms import GameForm, CropsForm, BudgetForm, DebtForm, EndTurnForm

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
            return g[0].turn_set.order_by('-turn')[0]
    
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
        """if new_genfund-wb_int-wbsap_int > 0:
            #may not continue until your budget is balanced (with exception of World Bank interest)
            if turn == 1:
                #tutorial: should probably go back to the Crops page and make some more changes
        else:
            if new_genfund < 0:
                #not enough income to cover expenses
                #World Bank will loan with SAP to cover interest payments on World Bank loans
            else:
                if genhap <= 30 and random.random() <= 1.1559*math.exp(-0.0741*genhap) and turn > 3:
                    #set voted out flag to true
                elif egenhap <= 30 and random.random() <= 1.1559*exp(-0.0741*egenhap) and turn > 3 and land >= 100:
                    #reduce turn.land
                    #reallocate crops in same proportions if necessary
                    #set decapitalized flag to true
                if wboacc = "Yes"$
                    #check SAP funding limits
                    if cocoa < 750:
                        #plant up to min(750,land) cocoa
                        #add cost to new WB SAP loan
                    #new loan = -new_genfund + cocoa planting cost
                    #new_genfund = 0
                #update land productivity for pesticides type
                #create new turn
                turn.save()
                turn.pk = None
                turn.turn += 1
                turn.save()
        #turn = form.save(commit=False)
        #turn.save()
        #return redirect(reverse_lazy('deveconsim:index'))
        """
        return super(EndTurnUpdateView, self).form_valid(form)

