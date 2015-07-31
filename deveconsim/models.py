from django.db import models
from django.contrib.auth.models import User
import math
from django.core.validators import MinValueValidator, MaxValueValidator

class Game(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    started_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True,null=True)
    
    #game constants
    INT_RATE = {'private':.0875, 'wb':.0715, 'wbsap':.0715}
    POP = {'l':4950000, 'u':50000}
    SVC_MAX = {'health':450*10**6, 'education':400*10**6, 'security':900*10**6}
    HAPPINESS = {'l':{'lfood':.20,'llux':.15,'ltax':.16,'health':.14,'education':.14,'security':.14,'env':.07}, #weightings
                 'u':{'ufood':.06,'ulux':.25,'utax':.22,'health':.10,'education':.10,'security':.24,'env':.03}}
    CROPS = {'corn':{'planting_cost':100, 'labor_cost':125, 'other_cost':25, 'pesticides':[{'cost':0,'yield':1500},{'cost':350,'yield':5000},{'cost':550,'yield':6000}], 'prices':[0.110,0.106,0.100,0.108,0.102,0.110,0.108,0.108,0.106,0.108,0.108,0.108,0.110,0.108,0.106,0.108,0.102,0.110,0.102,0.106,0.106,0.102,0.104,0.102,0.110,0.106,0.110,0.106,0.106,0.104,0.100,0.104,0.100,0.108,0.100,0.102,0.108,0.106,0.106,0.110,0.102,0.104,0.108,0.108,0.108,0.102,0.104,0.106,0.108,0.108,0.100,0.104,0.106,0.102,0.106,0.104,0.108,0.100,0.106,0.102,0.102,0.106,0.102,0.102,0.104,0.100,0.100,0.100,0.106,0.106,0.110,0.108,0.106,0.102,0.106,0.110,0.102,0.106,0.104,0.110,0.110,0.102,0.110,0.104,0.100,0.100,0.104,0.108,0.102,0.100,0.106,0.100,0.102,0.108,0.102,0.102,0.104,0.110,0.110,0.110,0.105]},
             'cocoa':{'planting_cost':500, 'labor_cost':175, 'other_cost':175, 'pesticides':[{'cost':0,'yield':500},{'cost':350,'yield':850},{'cost':450,'yield':1000}], 'prices':[3.85,3.41,3.30,2.64,2.09,2.42,2.20,2.09,1.98,1.54,1.32,1.21,1.27,1.21,1.14,1.07,1.06,1.06,1.07,1.10,1.04,0.96,0.91,0.95,0.95,1.03,1.06,1.05,1.11,1.08,1.03,1.02,0.94,0.94,0.94,0.91,0.99,1.07,1.11,1.17,1.11,1.03,0.96,0.92,0.94,0.94,0.90,0.94,1.01,0.99,0.91,0.95,0.97,1.05,1.04,1.00,1.08,1.00,1.07,1.10,1.17,1.22,1.22,1.14,1.20,1.21,1.17,1.09,1.07,1.07,1.07,1.06,1.10,1.04,1.10,1.05,0.99,1.04,1.08,1.08,1.15,1.18,1.12,1.19,1.19,1.26,1.26,1.20,1.25,1.27,1.27,1.21,1.28,1.29,1.29,1.21,1.23,1.18,1.11,1.12,1.10]}}
    PESTICIDES = [{'unhappiness':0, 'prod_loss':0},
                  {'unhappiness':20, 'prod_loss':.04},
                  {'unhappiness':5, 'prod_loss':.02}]
    HAPPINESS_WEIGHTS = [3,2.4,1.9,1.6,1.4,1.2,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.5,1.6,1.7,1.85,2]
                  
    def __str__(self):
        return 'Game "{2}" started {1} on {0:%m}/{0:%d}/{0:%y} at {0:%H}:{0:%M}'.format(self.started_date, 'by {0}'.format(self.user) if self.user else 'anonymously', self.name)
        
    def hapw(self,h):
        return self.HAPPINESS_WEIGHTS[int(min(1,h)*(len(self.HAPPINESS_WEIGHTS)-1))]

class Turn(models.Model):
    game = models.ForeignKey(Game)
    turn = models.PositiveIntegerField(default=1)
    started_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True,null=True)

    PESTICIDE_CHOICES = ((0,'None'),(1,'Cheap'),(2,'Expensive'),)
    
    #defaults are for turn 1
    genfund = models.PositiveIntegerField(default=20*10**6)
    debt_private = models.PositiveIntegerField(default=250*10**6)
    debt_wb = models.PositiveIntegerField(default=750*10**6)
    debt_wbsap = models.PositiveIntegerField(default=0)
    debt_repay_private = models.PositiveIntegerField(default=0)
    debt_repay_wb = models.PositiveIntegerField(default=0)
    debt_repay_wbsap = models.PositiveIntegerField(default=0)
    debt_new_wbsap = models.PositiveIntegerField(default=0)
    tax_cocoa = models.PositiveSmallIntegerField(default=10, validators=[MaxValueValidator(30)])
    tax_lower = models.PositiveSmallIntegerField(default=20, validators=[MaxValueValidator(70)])
    tax_upper = models.PositiveSmallIntegerField(default=30, validators=[MaxValueValidator(70)])
    svc_health = models.PositiveSmallIntegerField(default=25, validators=[MaxValueValidator(100)])
    svc_education = models.PositiveSmallIntegerField(default=25, validators=[MaxValueValidator(100)])
    svc_security = models.PositiveSmallIntegerField(default=35, validators=[MaxValueValidator(100)])
    land = models.PositiveIntegerField(default=10**3)
    start_corn = models.PositiveIntegerField(default=900)
    start_cocoa = models.PositiveIntegerField(default=100)
    corn = models.PositiveIntegerField(default=900)
    cocoa = models.PositiveIntegerField(default=100)
    landprod = models.FloatField(default=1., validators=[MaxValueValidator(0), MaxValueValidator(1)])
    pesticides = models.PositiveSmallIntegerField(choices=PESTICIDE_CHOICES, default=0)
    voted_out = models.BooleanField(default=False)
    decapitalized = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('game', 'turn',)
        
    def __str__(self):
        return 'Turn {0} ({1})'.format(self.turn, self.game)
    
    def calc(self):
        g = self.game #shortcut
        r = {} #results
        
        #crop calculations
        r['start_unplanted'] = self.land-self.start_corn-self.start_cocoa
        r['unplanted'] = self.land-self.corn-self.cocoa
        for c in g.CROPS.keys():
            r[c] = {}
            r[c]['price'] = g.CROPS[c]['prices'][min(self.turn,len(g.CROPS[c]['prices']))-1]
            r[c]['yield'] = g.CROPS[c]['pesticides'][self.pesticides]['yield']*self.landprod #cny, ccy
            r[c]['inc'] = getattr(self,c)*1000*r[c]['yield']*r[c]['price'] #cninc, ccinc
            r[c]['exp'] = -getattr(self,c)*1000*(g.CROPS[c]['pesticides'][self.pesticides]['cost']+g.CROPS[c]['labor_cost']+g.CROPS[c]['other_cost']) #cngc, ccgc
            r[c]['net'] = r[c]['inc']*(.85-self.tax_cocoa/100 if c=='cocoa' else 1)+r[c]['exp'] #cnginc, ccginc
        
        #debt calculations
        for k,v in g.INT_RATE.items():
            r['debt_{0}_int'.format(k)] = getattr(self,'debt_'+k)*v
        r['debt_total'] = self.debt_private+self.debt_wb+self.debt_wbsap
        r['debt_total_int'] = r['debt_private_int']+r['debt_wb_int']+r['debt_wbsap_int']
        
        #budget calculations
        lbinc = sum(getattr(self,c)*1000*g.CROPS[c]['labor_cost'] for c in g.CROPS.keys())
        ubinc = sum(r[c]['net'] for c in g.CROPS.keys())
        r['inc_cocoa'] = max(0,r['cocoa']['inc']*self.tax_cocoa/100) #cctinc
        r['inc_lower'] = max(0,lbinc*self.tax_lower/100) #lbitinc
        r['inc_upper'] = max(0,ubinc*self.tax_upper/100) #ubitinc
        r['inc_total'] = r['inc_cocoa']+r['inc_lower']+r['inc_upper']
        for k,v in g.SVC_MAX.items():
            r['exp_{0}'.format(k)] = -v*getattr(self,'svc_'+k)/100
        r['exp_debt_int'] = -r['debt_total_int']
        r['exp_plant_crops'] = -sum(max(0,getattr(self,c)-getattr(self,'start_'+c))*1000*g.CROPS[c]['planting_cost'] for c in g.CROPS.keys())
        r['exp_total'] = r['exp_health']+r['exp_education']+r['exp_security']+r['exp_debt_int']+r['exp_plant_crops']
        r['net'] = r['inc_total']+r['exp_total']
        r['new_genfund'] = self.genfund+r['net']
        
        #happiness calculations
        lbatinc = max(0,lbinc*(1-self.tax_lower/100-0.1)/g.POP['l'])
        ubatinc = max(0,ubinc*(1-self.tax_upper/100-0.05)/g.POP['u'])
        lcntobuy = min(int(lbatinc**.5/2)-7,68)*100 if lbatinc >= 400 else min(200,int(lbatinc/r['corn']['price']))
        ucntobuy = min(int(ubatinc**.5/2)-7,68)*100 if ubatinc >= 400 else min(200,int(ubatinc/r['corn']['price']))
        r['hap_lfood'] = max(0,.0175*1.017**lcntobuy if lcntobuy < 190 else .125*math.log(lcntobuy)-.225)
        r['hap_ufood'] = max(0,.0175*1.017**ucntobuy if ucntobuy < 190 else .125*math.log(ucntobuy)-.225)
        r['hap_llux'] = max(0,.125*math.log(max(1,lbatinc-lcntobuy*r['corn']['price']))-.575)
        r['hap_ulux'] = max(0,.135*math.log(max(1,ubatinc-ucntobuy*r['corn']['price']))-.6)
        r['hap_ltax'] = max(0,.9-self.tax_lower*.018) if self.tax_lower else 1
        r['hap_utax'] = max(0,.9-self.tax_upper*.024) if self.tax_upper else 1
        r['hap_health'] = self.svc_health/100
        r['hap_education'] = self.svc_education/100
        r['hap_security'] = self.svc_security/100
        r['hap_env'] = max(0,.9-.02*g.PESTICIDES[self.pesticides]['unhappiness'])
        r['hap_lgen'] = sum(r['hap_'+k]*g.hapw(r['hap_'+k])*v for k,v in g.HAPPINESS['l'].items())/sum(g.hapw(r['hap_'+k]) for k in g.HAPPINESS['l'].keys())*7
        r['hap_ugen'] = sum(r['hap_'+k]*g.hapw(r['hap_'+k])*v for k,v in g.HAPPINESS['u'].items())/sum(g.hapw(r['hap_'+k]) for k in g.HAPPINESS['u'].keys())*7
        
        return r
