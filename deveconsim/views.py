from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import math
import random
from .models import Game, Turn

def hapw(hap):
	hapa = [3,2.4,1.9,1.6,1.4,1.2,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.85,2]
	return hapa[int(hap*20)]

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
    turn = Turn.objects.all()[0]
    g = turn.game #shortcut
    calc = turn.calc()
    
    
    lbinc = sum(getattr(turn,c)*g.CROPS[c]['labor_cost'] for c in g.CROPS.keys())
    ubinc = sum(calc[c]['net'] for c in g.CROPS.keys())
    
    inc = {}
    inc['cocoa'] = max(0,calc['cocoa']['inc']*turn.tax_cocoa/100) #cctinc
    inc['lower'] = max(0,lbinc*turn.tax_lower/100) #lbitinc
    inc['upper'] = max(0,ubinc*turn.tax_upper/100) #ubitinc
    inc['total'] = sum(inc.values())

    debt = {}
    debt['total'] = turn.debt_private+turn.debt_wb+turn.debt_wbsap
    debt['int'] = dict((k,getattr(turn,'debt_'+k)*g.INT_RATE[k]/100) for k in g.INT_RATE.keys())
    debt['int']['total'] = sum(debt['int'].values())
    
    exp = dict((k,-v*getattr(turn,'svc_'+k)/100) for k,v in g.SVC_MAX.items()) #hlexp, edexp, scexp
    exp['total'] = sum(exp.values())+debt['int']['total']
    
    budget = {}
    budget['inc'] = inc
    budget['exp'] = exp
    budget['debt_int'] = -debt['int']['total']
    budget['net'] = inc['total']+exp['total']
    budget['genfund_next'] = turn.genfund+budget['net']
    
    lbatinc = max(0,lbinc*(1-turn.tax_lower/100-0.1)/g.POP['l'])
    ubatinc = max(0,ubinc*(1-turn.tax_upper/100-0.05)/g.POP['u'])
    cntobuy = min(int(lbatinc**.5/2)-7,68)*100 if lbatinc >= 400 else min(200,int(lbatinc/calc['corn']['price']))
    ecntobuy = min(int(ubatinc**.5/2)-7,68)*100 if ubatinc >= 400 else min(200,int(ubatinc/calc['corn']['price']))
    
    hap = {}
    hap['lfood'] = max(0,1.75*1.017**cntobuy if cntobuy < 190 else 12.5*math.log(cntobuy)-22.5)/100
    hap['ufood'] = max(0,1.75*1.017**ecntobuy if ecntobuy < 190 else 12.5*math.log(ecntobuy)-22.5)/100
    hap['llux'] = max(0,12.5*math.log(max(1,lbatinc-cntobuy*calc['corn']['price']))-57.5)/100
    hap['ulux'] = max(0,13.5*math.log(max(1,ubatinc-ecntobuy*calc['corn']['price']))-60)/100
    hap['ltax'] = max(0,.9-turn.tax_lower*.018) if turn.tax_lower else 1
    hap['utax'] = max(0,.9-turn.tax_upper*.024) if turn.tax_upper else 1
    hap['health'] = turn.svc_health/100
    hap['education'] = turn.svc_education/100
    hap['security'] = turn.svc_security/100
    hap['env'] = max(0,.9-.02*g.PESTICIDES[turn.pesticides]['unhappiness'])
    hap['lgen'] = sum(hap[k]*hapw(hap[k])*v for k,v in g.HAPPINESS['l'].items())/sum(hapw(hap[k]) for k in g.HAPPINESS['l'].keys())*7
    hap['ugen'] = sum(hap[k]*hapw(hap[k])*v for k,v in g.HAPPINESS['u'].items())/sum(hapw(hap[k]) for k in g.HAPPINESS['u'].keys())*7
    

    return render(request, 'deveconsim/index.html', {'turn':turn, 'calc':calc, 'budget':budget, 'debt':debt, 'hap':hap})
