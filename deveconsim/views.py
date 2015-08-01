from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import View
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
        context['form'] = CropsForm(instance=context['turn'])
        return render(request, self.template, context)
    
    def post_actions(self, request, context):
        form = CropsForm(request.POST, instance=context['turn'])
        if form.is_valid():
            turn = form.save(commit=False)
            turn.save()
            return redirect(reverse('deveconsim:index'))
        else:
            context['calc'] = context['turn'].calc()
            context['form'] = form
            return render(request, self.template, context)
        
class BudgetView(TurnView):
    template = 'deveconsim/budget.html'
    
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        context['form'] = BudgetForm(instance=context['turn'])
        return render(request, self.template, context)
    
    def post_actions(self, request, context):
        form = BudgetForm(request.POST, instance=context['turn'])
        if form.is_valid():
            turn = form.save(commit=False)
            turn.save()
            return redirect(reverse('deveconsim:index'))
        else:
            context['calc'] = context['turn'].calc()
            context['form'] = form
            return render(request, self.template, context)
            
class DebtView(TurnView):
    template = 'deveconsim/debt.html'
    
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        context['form'] = DebtForm(instance=context['turn'])
        return render(request, self.template, context)
    
    def post_actions(self, request, context):
        form = DebtForm(request.POST, instance=context['turn'])
        if form.is_valid():
            turn = form.save(commit=False)
            turn.save()
            return redirect(reverse('deveconsim:index'))
        else:
            context['calc'] = context['turn'].calc()
            context['form'] = form
            return render(request, self.template, context)
            
class EndTurnView(TurnView):
    template = 'deveconsim/endturn.html'
    
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        context['form'] = EndTurnForm(instance=context['turn'])
        return render(request, self.template, context)
    
    def post_actions(self, request, context):
        form = EndTurnForm(request.POST, instance=context['turn'])
        if form.is_valid():
            """if corn+cocoa > land:
                #check land constraint
            if debt_wbsap:
                #check SAP funding limits
            if new_genfund-wb_int-wbsap_int > 0:
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
            #return redirect(reverse('deveconsim:index'))
            """
        else:
            context['calc'] = context['turn'].calc()
            context['form'] = form
            return render(request, self.template, context)

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
            