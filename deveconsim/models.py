import math

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from . import constants

class Game(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True, max_length=200)
    started_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True,null=True)
    
    success_url_str = 'deveconsim:index'
    start_url_str = 'deveconsim:start'
    session_pk_var = 'deveconsim_game_pk'
                  
    def __str__(self):
        return 'Game "{2}" started {1} on {0:%m}/{0:%d}/{0:%y} at {0:%H}:{0:%M}'.format(self.started_date, 'by {0}'.format(self.user) if self.user else 'anonymously', self.name)
        
    def last_turn(self):
        return self.turn_set.order_by('-turn')[0]

class Turn(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    turn = models.PositiveIntegerField(default=1)
    started_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True,null=True)
    
    #defaults are for turn 1
    genfund = models.PositiveIntegerField(default=20*10**6)
    debt_private = models.PositiveIntegerField(default=250*10**6)
    debt_wb = models.PositiveIntegerField(default=750*10**6)
    debt_wbsap = models.PositiveIntegerField(default=0)
    debt_repay_private = models.PositiveIntegerField(default=0, verbose_name='Repay Private Debt')
    debt_repay_wb = models.PositiveIntegerField(default=0, verbose_name='Repay World Bank Debt')
    debt_repay_wbsap = models.PositiveIntegerField(default=0, verbose_name='Repay World Bank SAP Debt')
    debt_new_wbsap = models.PositiveIntegerField(default=0, verbose_name='New World Bank SAP Debt')
    tax_cocoa = models.PositiveSmallIntegerField(default=10, verbose_name='Cocoa Tax', validators=[MaxValueValidator(30, message='Maximum is 30%%.')])
    tax_lower = models.PositiveSmallIntegerField(default=20, verbose_name='Income Tax - Lower Bracket', validators=[MaxValueValidator(70, message='Maximum is 70%%.')])
    tax_upper = models.PositiveSmallIntegerField(default=30, verbose_name='Income Tax - Upper Bracket', validators=[MaxValueValidator(70, message='Maximum is 70%%.')])
    svc_health = models.PositiveSmallIntegerField(default=25, verbose_name='Healthcare Funding', validators=[MaxValueValidator(100, message='Maximum is 100%%.')])
    svc_education = models.PositiveSmallIntegerField(default=25, verbose_name='Education Funding', validators=[MaxValueValidator(100, message='Maximum is 100%%.')])
    svc_security = models.PositiveSmallIntegerField(default=35, verbose_name='Security Funding', validators=[MaxValueValidator(100, message='Maximum is 100%%.')])
    land = models.PositiveIntegerField(default=10**3)
    start_corn = models.PositiveIntegerField(default=900)
    start_cocoa = models.PositiveIntegerField(default=100)
    corn = models.PositiveIntegerField(default=900)
    cocoa = models.PositiveIntegerField(default=100)
    wbsap_cocoa = models.PositiveIntegerField(default=0)
    landprod = models.FloatField(default=1., validators=[MinValueValidator(0), MaxValueValidator(1)])
    pesticides = models.PositiveSmallIntegerField(choices=constants.PESTICIDE_CHOICES, default=0)
    voted_out = models.BooleanField(default=False)
    decapitalized = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('game', 'turn',)
        
    def __str__(self):
        return 'Turn {0} ({1})'.format(self.turn, self.game)
    
    def calc(self):
        r = {} #results
        
        #crop calculations
        r['start_unplanted'] = self.land-self.start_corn-self.start_cocoa
        r['unplanted'] = self.land-self.corn-self.cocoa
        for c in constants.CROPS.keys():
            r[c] = {}
            r[c]['price'] = constants.CROPS[c]['prices'][min(self.turn,len(constants.CROPS[c]['prices']))-1]
            r[c]['yield'] = constants.CROPS[c]['pesticides'][self.pesticides]['yield']*self.landprod #cny, ccy
            r[c]['inc'] = getattr(self,c)*1000*r[c]['yield']*r[c]['price'] #cninc, ccinc
            r[c]['exp'] = -getattr(self,c)*1000*(constants.CROPS[c]['pesticides'][self.pesticides]['cost']+constants.CROPS[c]['labor_cost']+constants.CROPS[c]['other_cost']) #cngc, ccgc
            r[c]['net'] = r[c]['inc']*(.85-self.tax_cocoa/100 if c=='cocoa' else 1)+r[c]['exp'] #cnginc, ccginc
        
        #debt calculations
        for k,v in constants.INTEREST_RATES.items():
            r['debt_{0}_int'.format(k)] = getattr(self,'debt_'+k)*v
        r['debt_total'] = self.debt_private+self.debt_wb+self.debt_wbsap
        r['debt_total_int'] = r['debt_private_int']+r['debt_wb_int']+r['debt_wbsap_int']
        r['debt_total_repay'] = self.debt_repay_private+self.debt_repay_wb+self.debt_repay_wbsap
        
        #budget calculations
        lbinc = sum(getattr(self,c)*1000*constants.CROPS[c]['labor_cost'] for c in constants.CROPS.keys())
        ubinc = sum(r[c]['net'] for c in constants.CROPS.keys())
        r['inc_cocoa'] = max(0,r['cocoa']['inc']*self.tax_cocoa/100) #cctinc
        r['inc_lower'] = max(0,lbinc*self.tax_lower/100) #lbitinc
        r['inc_upper'] = max(0,ubinc*self.tax_upper/100) #ubitinc
        r['inc_total'] = r['inc_cocoa']+r['inc_lower']+r['inc_upper']
        for k,v in constants.MAX_SERVICE_FUNDING.items():
            r['exp_{0}'.format(k)] = -v*getattr(self,'svc_'+k)/100
        r['exp_debt_int'] = -r['debt_total_int']
        r['exp_plant_crops'] = -sum(max(0,getattr(self,c)-getattr(self,'start_'+c))*1000*constants.CROPS[c]['planting_cost'] for c in constants.CROPS.keys())
        r['exp_total'] = r['exp_health']+r['exp_education']+r['exp_security']+r['exp_debt_int']+r['exp_plant_crops']
        r['net'] = r['inc_total']+r['exp_total']
        r['new_genfund'] = self.genfund+r['net']-r['debt_total_repay']
        r['wbsap_add_cocoa'] = max(0,750-self.cocoa)
        r['wbsap_add_cocoa_cost'] = r['wbsap_add_cocoa']*1000*constants.CROPS['cocoa']['planting_cost']
        r['debt_new_wbsap_max'] = math.ceil((r['debt_wb_int']+r['debt_wbsap_int']+r['wbsap_add_cocoa_cost'])/10**6)*10**6 if r['new_genfund']<0 else 0
        r['new_genfund_plus_max_wbsap'] = r['new_genfund']+r['debt_new_wbsap_max']
        r['debt_new_wbsap_min'] = math.ceil(min(r['debt_new_wbsap_max'],max(0,-r['new_genfund'])+r['wbsap_add_cocoa_cost'])/10**6)*10**6
        
        #happiness calculations
        lbatinc = max(0,lbinc*(1-self.tax_lower/100-0.1)/constants.POPULATION_BY_CLASS['l'])
        ubatinc = max(0,ubinc*(1-self.tax_upper/100-0.05)/constants.POPULATION_BY_CLASS['u'])
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
        r['hap_env'] = max(0,.9-.02*constants.PESTICIDES[self.pesticides]['unhappiness'])
        r['hap_lgen'] = sum(r['hap_'+k]*constants.happiness_intensity_weight(r['hap_'+k])*v for k,v in constants.GENERAL_HAPPINESS_WEIGHTS_BY_CLASS['l'].items())/sum(constants.happiness_intensity_weight(r['hap_'+k]) for k in constants.GENERAL_HAPPINESS_WEIGHTS_BY_CLASS['l'].keys())*7
        r['hap_ugen'] = sum(r['hap_'+k]*constants.happiness_intensity_weight(r['hap_'+k])*v for k,v in constants.GENERAL_HAPPINESS_WEIGHTS_BY_CLASS['u'].items())/sum(constants.happiness_intensity_weight(r['hap_'+k]) for k in constants.GENERAL_HAPPINESS_WEIGHTS_BY_CLASS['u'].keys())*7
        
        return r
