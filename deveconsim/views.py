from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import math

def hapw(hap):
	hapa = [3,2.4,1.9,1.6,1.4,1.2,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.85,2]
	return hapa[int(hap/5)]

@login_required
def index(request):
    #load constants
    pest_data = {'None':{'corn':{'cost':0,'yield':1500}, 'cocoa':{'cost':0,'yield':500}, 'unhappiness':0, 'prod_loss':0},
                'Cheap':{'corn':{'cost':350,'yield':5000}, 'cocoa':{'cost':350,'yield':850}, 'unhappiness':20, 'prod_loss':.04},
                'Expensive':{'corn':{'cost':550,'yield':6000}, 'cocoa':{'cost':450,'yield':1000}, 'unhappiness':5, 'prod_loss':.02}}
    prices = {'corn':[0.110,0.106,0.100,0.108,0.102,0.110,0.108,0.108,0.106,0.108,0.108,0.108,0.110,0.108,0.106,0.108,0.102,0.110,0.102,0.106,0.106,0.102,0.104,0.102,0.110,0.106,0.110,0.106,0.106,0.104,0.100,0.104,0.100,0.108,0.100,0.102,0.108,0.106,0.106,0.110,0.102,0.104,0.108,0.108,0.108,0.102,0.104,0.106,0.108,0.108,0.100,0.104,0.106,0.102,0.106,0.104,0.108,0.100,0.106,0.102,0.102,0.106,0.102,0.102,0.104,0.100,0.100,0.100,0.106,0.106,0.110,0.108,0.106,0.102,0.106,0.110,0.102,0.106,0.104,0.110,0.110,0.102,0.110,0.104,0.100,0.100,0.104,0.108,0.102,0.100,0.106,0.100,0.102,0.108,0.102,0.102,0.104,0.110,0.110,0.110,0.105],
            'cocoa':[3.85,3.41,3.30,2.64,2.09,2.42,2.20,2.09,1.98,1.54,1.32,1.21,1.27,1.21,1.14,1.07,1.06,1.06,1.07,1.10,1.04,0.96,0.91,0.95,0.95,1.03,1.06,1.05,1.11,1.08,1.03,1.02,0.94,0.94,0.94,0.91,0.99,1.07,1.11,1.17,1.11,1.03,0.96,0.92,0.94,0.94,0.90,0.94,1.01,0.99,0.91,0.95,0.97,1.05,1.04,1.00,1.08,1.00,1.07,1.10,1.17,1.22,1.22,1.14,1.20,1.21,1.17,1.09,1.07,1.07,1.07,1.06,1.10,1.04,1.10,1.05,0.99,1.04,1.08,1.08,1.15,1.18,1.12,1.19,1.19,1.26,1.26,1.20,1.25,1.27,1.27,1.21,1.28,1.29,1.29,1.21,1.23,1.18,1.11,1.12,1.10]}
    crop_cost = {'corn':{'labor':125,'other':25}, #cncsta
                'cocoa':{'labor':175,'other':175}} #cccsta
    crop_list = ['corn','cocoa']
    int_rate = {'p':8.75, 's':7.15} #pintrate, sintrate
    svcmax = {'health':450000, 'education':400000, 'security':900000}
    mpop = 4950000 #MassesPopulation
    epop = 50000 #ElitePopulation
    genhapw = {'l':{'lfood':.2,'llux':.15,'ltax':.16,'health':.14,'education':.14,'security':.14,'env':.07},
                    'u':{'ufood':0.06,'ulux':.25,'utax':.22,'health':.1,'education':.1,'security':.24,'env':.03}}
	
    #load data for game instance
    genfund = 20000
    debt = {'p':250000, 's_list':[{'amt':250000,'sap':{'name':"Health <15%"}}, {'amt':500000,'sap':None}]} #pdebt, sdebt
    crops = {'land':1000000, 'corn':{'planted':900000}, 'cocoa':{'planted':100000}, 'landprod':100., 'pesticides':'None'}
    tax_rate = {'cocoa':10, 'lower':20, 'upper':30} #cct, lbit, ubit
    svc_rate = {'health':25, 'education':25, 'security':35} #hlf, edf, scf
    
    turn = 1
    
    crops['unplanted'] = crops['land']-crops['corn']['planted']-crops['cocoa']['planted']
    for c in crop_list:
        crops[c]['yield'] = pest_data[crops['pesticides']][c]['yield']*crops['landprod']/100 #cny, ccy
        crops[c]['price'] = prices[c][min([turn,len(prices[c])])-1] #cnprc, ccprc
        crops[c]['inc'] = crops[c]['planted']*crops[c]['yield']*crops[c]['price'] #cninc, ccinc
        crops[c]['exp'] = crops[c]['planted']*(pest_data[crops['pesticides']][c]['cost']+sum(crop_cost[c].values())) #cngc, ccgc
        crops[c]['net'] = crops[c]['inc']*(.85-tax_rate[c]/100 if c=='cocoa' else 1)-crops[c]['exp'] #cnginc, ccginc
    
    lbinc = sum(crops[c]['planted']*crop_cost[c]['labor'] for c in crop_list)
    ubinc = sum(crops[c]['net'] for c in crop_list)
    
    inc = {}
    inc['cocoa'] = max(0,crops['cocoa']['inc']*tax_rate['cocoa']/100/1000) #cctinc
    inc['lower'] = max(0,lbinc*tax_rate['lower']/100/1000) #lbitinc
    inc['upper'] = max(0,ubinc*tax_rate['upper']/100/1000) #ubitinc
    inc['total'] = sum(inc.values())

    debt['s'] = sum(d['amt'] for d in debt['s_list'])
    debt['int_rate'] = int_rate
    debt['total'] = debt['p']+debt['s']
    debt['int'] = dict((d,debt[d]*int_rate[d]/100) for d in ['p','s'])
    debt['int']['total'] = sum(debt['int'].values())
    debt['sap'] = defaultdict(int)
    for d in debt['s_list']:
        if d['sap']:
           debt['sap'][d['sap']['name']] += d['amt']
    debt['sap'] = dict(debt['sap'])
   
    exp = dict((svc,-svcmax[svc]*rate/100) for svc,rate in svc_rate.items()) #hlexp, edexp, scexp
    exp['total'] = sum(exp.values())+debt['int']['total']
    
    budget = {'tax_rate':tax_rate, 'inc':inc, 'svc_rate':svc_rate, 'exp':exp, 'genfund':genfund, 'net':inc['total']+exp['total']}
    budget['genfund_next'] = budget['genfund']+budget['net']
    
    lbatinc = max(0,lbinc*(1-tax_rate['lower']/100-0.1)/mpop)
    ubatinc = max(0,ubinc*(1-tax_rate['upper']/100-0.05)/epop)
    cntobuy = min(int(lbatinc**.5/2)-7,68)*100 if lbatinc >= 400 else min(200,int(lbatinc/crops['corn']['price']))
    ecntobuy = min(int(ubatinc**.5/2)-7,68)*100 if ubatinc >= 400 else min(200,int(ubatinc/crops['corn']['price']))
    
    hap = {}
    hap['lfood'] = max(0,1.75*1.017**cntobuy if cntobuy < 190 else 12.5*math.log(cntobuy)-22.5)
    hap['ufood'] = max(0,1.75*1.017**ecntobuy if ecntobuy < 190 else 12.5*math.log(ecntobuy)-22.5)
    hap['llux'] = max(0,12.5*math.log(max(1,lbatinc-cntobuy*crops['corn']['price']))-57.5)
    hap['ulux'] = max(0,13.5*math.log(max(1,ubatinc-ecntobuy*crops['corn']['price']))-60)
    hap['ltax'] = max(0,90-tax_rate['lower']*1.8) if tax_rate['lower'] else 100
    hap['utax'] = max(0,90-tax_rate['upper']*2.4) if tax_rate['upper'] else 100
    hap['health'] = svc_rate['health']
    hap['education'] = svc_rate['education']
    hap['security'] = svc_rate['security']
    hap['env'] = max(0,90-2*pest_data[crops['pesticides']]['unhappiness'])
    hap['lgen'] = sum(hap[k]*hapw(hap[k])*v for k,v in genhapw['l'].items())/sum(hapw(hap[k]) for k in genhapw['l'].keys())*7
    hap['ugen'] = sum(hap[k]*hapw(hap[k])*v for k,v in genhapw['u'].items())/sum(hapw(hap[k]) for k in genhapw['u'].keys())*7
    
    return render(request, 'deveconsim/index.html', {'turn':turn, 'budget':budget, 'crops':crops, 'debt':debt, 'hap':hap})
