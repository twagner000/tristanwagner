from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.decorators import login_required

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
        crops[c]['price'] = prices[c][min([turn,len(prices[c])])-1]
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
    
    return render(request, 'deveconsim/index.html', {'turn':turn, 'budget':budget, 'crops':crops, 'debt':debt})
