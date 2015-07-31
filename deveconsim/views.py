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
            pass
            """if yearend:
        #check for ongoing SAP requirements
        if debt['wbsap']:
            if svc_rate['health'] > 15:
                update_svc_rate('health',15)
            if svc_rate['security'] > 20:
                update_svc_rate('security',20)
        #check that general fund balances (World Bank interest is the exception)
        if budget['genfund_next']+debt['int']['wb']+debt['int']['wbsap'] > 0:
            if budget['genfund_next'] > 0 or accept_sap:
                #check for getting voted out or decapitalization
                if hap['lgen'] <= 15 and math.random() <= 1.1559*math.exp(-0.0741*hap['lgen']) and turn > 4:
                    votedout()
                elif hap['ugen'] <= 15 and math.random() <= 1.1559*exp(-0.0741*hap['ugen']) and turn > 4 and crops['land'] >= 100000:
                    decapitalize()
                if accept_sap:
                    #fulfill SAP requirements and take out loan
                    if svc_rate['health'] > 15:
                        update_svc_rate('health',15)
                    if svc_rate['security'] > 20:
                        update_svc_rate('security',20)
                    if crops['cocoa']['planted'] < 750000:
                        newloan = plant('cocoa',min(750000,crops['land'])-crops['cocoa']['planted'])
                    newloan -= budget['genfund_next']
                    budget['genfund_next'] = 0
            turn += 1
            nlandprod = landprod*(1-ped)"""
            #turn = form.save(commit=False)
            #turn.save()
            #return redirect(reverse('deveconsim:index'))
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
            