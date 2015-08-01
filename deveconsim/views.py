from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Game, Turn
from .forms import GameForm, CropsForm, BudgetForm, DebtForm, EndTurnForm

def votedout():
    #set voted out flag to true
    pass
    
def decapitalize():
    #reduce turn.land
    #reallocate crops in same proportions if necessary
    #set decapitalized flag to true
    pass

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

        
def fbv_open_games(request):
        g = Game.objects.filter(pk=request.session.get('deveconsim_game_pk', None), completed_date__isnull=True)
        if request.user.is_authenticated():
            g = g | Game.objects.filter(user=request.user, completed_date__isnull=True)
        return g
        
def start(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            for open_game in fbv_open_games(request):
                open_game.completed_date = timezone.now()
                open_game.save()
            game = form.save(commit=False)
            if request.user.is_authenticated():
                game.user = request.user
            game.save()
            game.turn_set.create()
            game.save()
            request.session['deveconsim_game_pk'] = game.pk
        return redirect(reverse_lazy('deveconsim:index'))
    else:
        form = GameForm()
        return render(request, 'deveconsim/start.html', {'form':form, 'open_games':fbv_open_games(request)})

def choose_open(request):
    og = fbv_open_games(request)
    if len(og) <= 1:
        return redirect(reverse_lazy('deveconsim:index'))
    else:
        if request.method == "POST":
            chosen_game = og.filter(pk=request.POST['game_pk'])
            if len(chosen_game) == 1:
                chosen_game = chosen_game[0]
                for open_game in og:
                    if open_game != chosen_game:
                        open_game.completed_date = timezone.now()
                    if request.user.is_authenticated():
                        open_game.user = request.user
                    open_game.save()
                request.session['deveconsim_game_pk'] = chosen_game.pk
                return redirect(reverse_lazy('deveconsim:index'))
            else:
                return render(request, 'deveconsim/choose_open.html', {'open_games':og.order_by('-started_date')})
        else:
            return render(request, 'deveconsim/choose_open.html', {'open_games':og.order_by('-started_date')})
            
        
class TurnDetailView(CurrentTurnMixin, DetailView):
    def get(self, request):
        if not hasattr(self,'object'):
            return redirect(reverse_lazy('deveconsim:start'))
        return super(TurnDetailView, self).get(request)
        
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
                    votedout()
                elif egenhap <= 30 and random.random() <= 1.1559*exp(-0.0741*egenhap) and turn > 3 and land >= 100:
                    decapitalize()
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

