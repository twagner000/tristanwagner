from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from .models import Turn

def votedout():
    #set voted out flag to true
    pass
    
def decapitalize():
    #reduce turn.land
    #reallocate crops in same proportions if necessary
    #set decapitalized flag to true
    pass
    
@login_required
def index(request):
    qs = Turn.objects.all()
    if qs:
        turn = qs[0]
        calc = turn.calc()
    else:
        turn = None
        calc = None
   
    return render(request, 'deveconsim/index.html', {'turn':turn, 'calc':calc})
