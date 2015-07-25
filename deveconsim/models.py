from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=200)
    started_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True,null=True)
    
    #game constants
    INT_RATE = {'private':8.75, 'wb':7.15, 'wbsap':7.15}
    POP = {'l':4950000, 'u':50000}
    SVC_MAX = {'health':450*10**6, 'education':400*10**6, 'security':900*10**6}
    HAPPINESS = {'l':{'lfood':.20,'llux':.15,'ltax':.16,'health':.14,'education':.14,'security':.14,'env':.07}, #weightings
                 'u':{'ufood':.06,'ulux':.25,'utax':.22,'health':.10,'education':.10,'security':.24,'env':.03}}
    CROPS = {'corn':{'planting_cost':100, 'labor_cost':125, 'other_cost':25, 'pesticides':[{'cost':0,'yield':1500},{'cost':350,'yield':5000},{'cost':550,'yield':6000}], 'prices':[0.110,0.106,0.100,0.108,0.102,0.110,0.108,0.108,0.106,0.108,0.108,0.108,0.110,0.108,0.106,0.108,0.102,0.110,0.102,0.106,0.106,0.102,0.104,0.102,0.110,0.106,0.110,0.106,0.106,0.104,0.100,0.104,0.100,0.108,0.100,0.102,0.108,0.106,0.106,0.110,0.102,0.104,0.108,0.108,0.108,0.102,0.104,0.106,0.108,0.108,0.100,0.104,0.106,0.102,0.106,0.104,0.108,0.100,0.106,0.102,0.102,0.106,0.102,0.102,0.104,0.100,0.100,0.100,0.106,0.106,0.110,0.108,0.106,0.102,0.106,0.110,0.102,0.106,0.104,0.110,0.110,0.102,0.110,0.104,0.100,0.100,0.104,0.108,0.102,0.100,0.106,0.100,0.102,0.108,0.102,0.102,0.104,0.110,0.110,0.110,0.105]},
             'cocoa':{'planting_cost':500, 'labor_cost':175, 'other_cost':175, 'pesticides':[{'cost':0,'yield':500},{'cost':350,'yield':850},{'cost':450,'yield':1000}], 'prices':[3.85,3.41,3.30,2.64,2.09,2.42,2.20,2.09,1.98,1.54,1.32,1.21,1.27,1.21,1.14,1.07,1.06,1.06,1.07,1.10,1.04,0.96,0.91,0.95,0.95,1.03,1.06,1.05,1.11,1.08,1.03,1.02,0.94,0.94,0.94,0.91,0.99,1.07,1.11,1.17,1.11,1.03,0.96,0.92,0.94,0.94,0.90,0.94,1.01,0.99,0.91,0.95,0.97,1.05,1.04,1.00,1.08,1.00,1.07,1.10,1.17,1.22,1.22,1.14,1.20,1.21,1.17,1.09,1.07,1.07,1.07,1.06,1.10,1.04,1.10,1.05,0.99,1.04,1.08,1.08,1.15,1.18,1.12,1.19,1.19,1.26,1.26,1.20,1.25,1.27,1.27,1.21,1.28,1.29,1.29,1.21,1.23,1.18,1.11,1.12,1.10]}}
    PESTICIDES = [{'unhappiness':0, 'prod_loss':0},
                  {'unhappiness':20, 'prod_loss':.04},
                  {'unhappiness':5, 'prod_loss':.02}]
                  
    def __str__(self):
        return 'Game started by {1} on {0:%m}/{0:%d}/{0:%y}'.format(self.started_date, self.user if self.user else '"{0}"'.format(self.name))

class Turn(models.Model):
    game = models.ForeignKey(Game)
    turn = models.PositiveIntegerField(default=1)
    started_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True,null=True)

    PESTICIDE_CHOICES = ((0,'None'),(1,'Cheap'),(2,'Expensive'),)
    
    #defaults are for turn 1
    genfund = models.PositiveIntegerField(default=20*10**6)
    debt_private = models.PositiveIntegerField(default=250*10**6)
    debt_wb = models.PositiveIntegerField(default=500*10**6)
    debt_wbsap = models.PositiveIntegerField(default=250*10**6)
    tax_cocoa = models.PositiveSmallIntegerField(default=10)
    tax_lower = models.PositiveSmallIntegerField(default=20)
    tax_upper = models.PositiveSmallIntegerField(default=30)
    svc_health = models.PositiveSmallIntegerField(default=25)
    svc_education = models.PositiveSmallIntegerField(default=25)
    svc_security = models.PositiveSmallIntegerField(default=35)
    land = models.PositiveIntegerField(default=10**6)
    corn = models.PositiveIntegerField(default=900*10**3)
    cocoa = models.PositiveIntegerField(default=100*10**3)
    landprod = models.FloatField(default=1.)
    pesticides = models.PositiveSmallIntegerField(choices=PESTICIDE_CHOICES, default=0)
    
    class Meta:
        unique_together = ('game', 'turn',)
        
    def __str__(self):
        return 'Turn {0} ({1})'.format(self.turn, self.game)
    
    def calc(self):
        g = self.game #shortcut
        r = {} #results
        r['unplanted'] = self.land-self.corn-self.cocoa
        for c in g.CROPS.keys():
            r[c] = {}
            r[c]['price'] = g.CROPS[c]['prices'][min(self.turn,len(g.CROPS[c]['prices']))-1]
            r[c]['yield'] = g.CROPS[c]['pesticides'][self.pesticides]['yield']*self.landprod #cny, ccy
            r[c]['inc'] = getattr(self,c)*r[c]['yield']*r[c]['price'] #cninc, ccinc
            r[c]['exp'] = getattr(self,c)*(g.CROPS[c]['pesticides'][self.pesticides]['cost']+g.CROPS[c]['labor_cost']+g.CROPS[c]['other_cost']) #cngc, ccgc
            r[c]['net'] = r[c]['inc']*(.85-self.tax_cocoa/100 if c=='cocoa' else 1)-r[c]['exp'] #cnginc, ccginc
        
        return r
