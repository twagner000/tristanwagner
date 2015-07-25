from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic import View
from .models import Game, Turn
from .forms import GameForm

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
    def get_actions(self, request, context):
        return context
    def get(self, request):
        og = open_games(request)
        if len(og) > 1:
            return redirect(reverse('deveconsim:choose_open'))
        elif not og:
            return redirect(reverse('deveconsim:start'))
        else:
            turn = og[0].turn_set.order_by('-turn')[0]
            return render(request, self.template, self.get_actions(request, {'turn':turn}))

class IndexView(TurnView):
    template = 'deveconsim/index.html'
    def get_actions(self, request, context):
        context['calc'] = context['turn'].calc()
        return context        

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
            