from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import View
from .models import Game, Turn
from .forms import GameForm, CropsForm, BudgetForm

def votedout():
    #set voted out flag to true
    pass
    
def decapitalize():
    #reduce turn.land
    #reallocate crops in same proportions if necessary
    #set decapitalized flag to true
    pass
    
def open_games(request):
    g = Game.objects.filter(pk=request.session.get('deveconsim_game_pk', None), completed_date__isnull=True)
    if request.user.is_authenticated():
        g = g | Game.objects.filter(user=request.user, completed_date__isnull=True)
    return g

class TurnView(View):
    template = None
    def turn(self, request, post=False):
        og = open_games(request)
        if len(og) > 1:
            return redirect(reverse('deveconsim:choose_open'))
        elif not og:
            return redirect(reverse('deveconsim:start'))
        else:
            turn = og[0].turn_set.order_by('-turn')[0]
            return self.post_actions(request, {'turn':turn}) if post else self.get_actions(request, {'turn':turn})
    def get_actions(self, request, context):
        return render(request, self.template, context)
    def post_actions(self, request, context):
        return render(request, self.template, context)
    def get(self, request):
        return self.turn(request)
    def post(self, request):
        return self.turn(request, True)

class IndexView(TurnView):
    template = 'deveconsim/index.html'
    
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        return render(request, self.template, context)

class CropsView(TurnView):
    template = 'deveconsim/crops.html'
    
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        context['crops_form'] = CropsForm(instance=context['turn'])
        return render(request, self.template, context)
    
    def post_actions(self, request, context):
        form = CropsForm(request.POST, instance=context['turn'])
        if form.is_valid():
            #You must plant at least 10,000 ha.
            #You only have ??? ha of non-[crop] land to plant; you can't plant more than that.
            #You only have turn.genfund in your country's General Fund right now -- you need $??? to plant ??? new ha of [crop].
            #You cannot take loans of less than $0 or of more than the total cost of planting the cocoa!
            #The World Bank only offers loans for planting Cocoa.
            #In order to plant ??? ha of [crop], you will need to remove ??? ha of [othercrop].
            #Planting ??? ha of [crop] will cost $???. Your country currently has $??? in its General Fund. You will need to take a $??? loan from the World Bank in order to have enough money to plant all of this cocoa. If you wish, you may take a bigger loan (up to 100% of the amount needed).
            turn = form.save(commit=False)
            turn.save()
            return redirect(reverse('deveconsim:index'))
        return self.get_actions(request, context)
        
class BudgetView(TurnView):
    template = 'deveconsim/budget.html'
    
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        context['budget_form'] = BudgetForm(instance=context['turn'])
        return render(request, self.template, context)
    
    def post_actions(self, request, context):
        form = BudgetForm(request.POST, instance=context['turn'])
        if form.is_valid():
            turn = form.save(commit=False)
            turn.save()
            return redirect(reverse('deveconsim:index'))
        return self.get_actions(request, context)

def start(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            for open_game in open_games(request):
                open_game.completed_date = timezone.now()
                open_game.save()
            game = form.save(commit=False)
            if request.user.is_authenticated():
                game.user = request.user
            game.save()
            game.turn_set.create()
            game.save()
            request.session['deveconsim_game_pk'] = game.pk
        return redirect(reverse('deveconsim:index'))
    else:
        form = GameForm()
        return render(request, 'deveconsim/start.html', {'form':form, 'open_games':open_games(request)})

def choose_open(request):
    og = open_games(request)
    if len(og) <= 1:
        return redirect(reverse('deveconsim:index'))
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
                return redirect(reverse('deveconsim:index'))
            else:
                return render(request, 'deveconsim/choose_open.html', {'open_games':og.order_by('-started_date')})
        else:
            return render(request, 'deveconsim/choose_open.html', {'open_games':og.order_by('-started_date')})
            