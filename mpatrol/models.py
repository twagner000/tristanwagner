from django.db import models
from django.contrib.auth.models import User

from . import constants

class Game(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    started_date = models.DateTimeField(auto_now_add=True)
    ended_date = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return 'Game "{1}" started on {0:%m}/{0:%d}/{0:%y}'.format(self.started_date, self.name)
        
    #each real day is 2 months in game time
        
    
class Player(models.Model):
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    started_date = models.DateTimeField(auto_now_add=True)
    last_action_date = models.DateTimeField(blank=True, null=True)
    
    ll = models.PositiveSmallIntegerField(default=1, verbose_name='Leader Level')
    gold = models.PositiveIntegerField(default=100)
    xp = models.PositiveIntegerField(default=0, verbose_name='Experience')
    
    #Techs
    #Structures
    #medals = models.PositiveSmallIntegerField(default=0)
    #missions_completed = models.PositiveSmallIntegerField(default=0)
    #Special Abilities
    #Allies (Up to 10)
    
    class Meta:
        unique_together = ('game', 'user',)
        
    def __str__(self):
        return 'Player {0} in {1}'.format(self.user, self.game)
    
    def calc(self):
        r = {}
        r['life'] = constants.LEADER_LEVELS[self.ll]['life']
        battalion_calc = [b.calc() for b in self.battalion_set.all()]
        r['cp_avail'] = constants.LEADER_LEVELS[self.ll]['cp']-sum(b.get('cost_cp',0) for b in battalion_calc)
        r['attack'] = (1+self.ll/10)*sum(b.get('attack',0) for b in battalion_calc)
        r['defense'] = (1+self.ll/10)*sum(b.get('defense',0) for b in battalion_calc)
        r['oversee'] = sum(b.get('oversee',0) for b in battalion_calc)
        r['work_xp'] = sum(b.get('work_xp',0) for b in battalion_calc)
        gold_mult = max(1,2-(sum(b['count'] for b in battalion_calc)/r['oversee']) if r['oversee']>0 else 1)
        r['work_gold'] = gold_mult*sum(b.get('work_gold',0) for b in battalion_calc)
        #payday variable can also add +100 gold, but doesn't show up anywhere?
        return r
        
    def battles_fought(self):
        return self.attacker_set.all() | self.defender_set.all()

        
class Battalion(models.Model):
    player = models.ForeignKey(Player)
    battalion_number = models.PositiveSmallIntegerField(default=1)
    creature_type = models.CharField(max_length=50, choices=tuple((v,v) for v in constants.CREATURES.keys()), blank=True)
    count = models.PositiveSmallIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    weapon_base = models.CharField(max_length=50, choices=tuple((v,v) for v in constants.WEAPON_BASES.keys()), blank=True)
    weapon_material = models.CharField(max_length=50, choices=tuple((v,v) for v in constants.WEAPON_MATERIALS.keys()), blank=True)
    
    class Meta:
        unique_together = ('player', 'battalion_number',)
        ordering = ['battalion_number']
        
    def __str__(self):
        return 'Battalion {0}, {1}'.format(self.battalion_number, self.player)
        
    def calc(self):
        r = {}
        r['count'] = self.count
        creature = constants.CREATURES.get(self.creature_type)
        if creature:
            r['cost_cp'] = self.count*creature['cost_cp']
            r['work_gold'] = self.count*creature['work_gold']
            r['work_xp'] = self.count*creature['work_xp']
            r['oversee'] = self.count*creature['oversee']
            r['attack'] = (1+self.level/10)*self.count*creature['attack']
            r['defense'] = (1+self.level/10)*self.count*creature['defense']
            #apply weapon multipliers
            weapon_base = constants.WEAPON_BASES.get(self.weapon_base)
            weapon_material = constants.WEAPON_MATERIALS.get(self.weapon_material)
            if weapon_base and weapon_material:
                r['attack'] *= weapon_base['attack_mult']*weapon_material['attack_mult']
                r['defense'] *= weapon_material['armor']
            
        return r
    

class Message(models.Model):
    #see messages.e.txt
    sender = models.ForeignKey(Player,related_name='sender_set',null=True)
    recipient = models.ForeignKey(Player,related_name='recipient_set')
    sent_date = models.DateTimeField(auto_now_add=True)
    subject = models.TextField()
    message = models.TextField(blank=True)
    unread = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-sent_date']
    
    def __str__(self):
        return 'Message "{0}" from {1} to {2}'.format(self.subject, self.sender, self.recipient)
    
    
class Battle(models.Model):
    attacker = models.ForeignKey(Player,related_name='attacker_set')
    defender = models.ForeignKey(Player,related_name='defender_set')
    battle_date = models.DateTimeField(auto_now_add=True)
    successful_attack = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-battle_date']
    
    def __str__(self):
        return 'Battle {0} attacked {1} on {2}'.format(self.attacker, self.defender, self.battle_date)


