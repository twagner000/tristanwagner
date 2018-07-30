from django.db import models
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef, Sum
from django.core.exceptions import ObjectDoesNotExist
import collections
import datetime
import json
import math

from . import constants


class Game(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    started_date = models.DateTimeField(auto_now_add=True)
    #started_date.editable=True #for testing only
    ended_date = models.DateTimeField(blank=True,null=True)
    last_interest_date = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return '{1} (started {0:%m}/{0:%d}/{0:%y})'.format(self.started_date, self.name)
        
    
class LeaderLevel(models.Model):
    level = models.PositiveSmallIntegerField(unique=True)
    life = models.PositiveIntegerField(default=0)
    cp = models.PositiveIntegerField(default=0)
    cost_xp = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['level']
        
    def __str__(self):
        return str(self.level)
        
    def enabled_creatures(self):
        return Creature.objects.filter(min_ll=self.level)
        
    
class Creature(models.Model):
    name = models.CharField(unique=True, max_length=50)
    plural_name = models.CharField(max_length=50)
    min_ll = models.PositiveSmallIntegerField(default=1, verbose_name='Min Leader Level')
    attack = models.PositiveSmallIntegerField(default=0)
    defense = models.PositiveSmallIntegerField(default=0)
    cost_cp = models.PositiveSmallIntegerField(default=1, verbose_name='Cost in Creature Points')
    cost_gold = models.PositiveSmallIntegerField(default=20, verbose_name='Cost in Gold')
    work_gold = models.PositiveSmallIntegerField(default=5, verbose_name='Gold from Working')
    work_xp = models.PositiveSmallIntegerField(default=10, verbose_name='Experience from Working')
    oversee = models.PositiveSmallIntegerField(default=0, verbose_name='Overseeing Capability')
    
    class Meta:
        ordering = ['min_ll','cost_cp','cost_gold','work_gold','work_xp']
        
    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(unique=True, max_length=50)
    min_ll = models.PositiveSmallIntegerField(default=1, verbose_name='Min Leader Level')
    cost_xp = models.PositiveSmallIntegerField(default=100)
    prereq = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name='Prerequisite')
    
    class Meta:
        ordering = ['min_ll','cost_xp','name']
        
    def __str__(self):
        return self.name
        
    def prereq_names(self):
        return self.prereq.values_list('name', flat=True)


class Structure(models.Model):
    name = models.CharField(unique=True, max_length=50)
    cost_gold = models.PositiveSmallIntegerField(default=100)
    cost_xp = models.PositiveSmallIntegerField(default=100)
    tech_req = models.ForeignKey(Technology, models.PROTECT, null=True, blank=True, verbose_name='Required Technology')
    struct_req = models.ForeignKey('self', models.PROTECT, null=True, blank=True, verbose_name='Required Structure')
    effects = models.TextField(blank=True)
    interest_gold = models.PositiveSmallIntegerField(default=0)
    interest_xp = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['cost_gold','cost_xp','name']
        
    def __str__(self):
        return self.name
            
            
class WeaponBase(models.Model):
    name = models.CharField(unique=True, max_length=50)
    tech_req = models.ForeignKey(Technology, models.PROTECT, null=True, blank=True, verbose_name='Required Technology')
    struct_req = models.ForeignKey(Structure, models.PROTECT, null=True, blank=True, verbose_name='Required Structure')
    attack_mult = models.FloatField(default=1.0)
    cost_gold = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        ordering = ['cost_gold','name']
        
    def __str__(self):
        return self.name


class WeaponMaterial(models.Model):
    name = models.CharField(unique=True, max_length=50)
    tech_req = models.ForeignKey(Technology, models.PROTECT, null=True, blank=True, verbose_name='Required Technology')
    struct_req = models.ForeignKey(Structure, models.PROTECT, null=True, blank=True, verbose_name='Required Structure')
    attack_mult = models.FloatField(default=1.0)
    cost_mult = models.FloatField(default=1.0)
    armor = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        ordering = ['cost_mult','name']
        
    def __str__(self):
        return self.name


class Player(models.Model):
    game = models.ForeignKey(Game, models.CASCADE)
    user = models.ForeignKey(User, models.PROTECT)
    character_name = models.CharField(max_length=50)
    started_date = models.DateTimeField(auto_now_add=True)
    #started_date.editable=True #for testing only
    
    ll = models.ForeignKey(LeaderLevel, models.PROTECT, verbose_name='Leader Level')
    gold = models.PositiveIntegerField(default=100)
    xp = models.PositiveIntegerField(default=0, verbose_name='Experience')
    technologies = models.ManyToManyField(Technology, blank=True)
    structures = models.ManyToManyField(Structure, blank=True)
    static_score = models.PositiveIntegerField(default=0)
    score_last_updated = models.DateTimeField(null=True,blank=True)
    
    #medals, missions_completed, Special Abilities, Allies (Up to 10)
    
    class Meta:
        ordering = ['game','character_name']
        unique_together = (('game', 'user',), ('game','character_name'))
        
    def __str__(self):
        return str(self.user)
        
    def save(self, *args, **kwargs):
        try:
            self.ll
        except:
            self.ll = LeaderLevel.objects.get(level=1)
        self.static_score = self.calc_score()
        self.score_last_updated = datetime.datetime.now()
        super().save(*args, **kwargs)
    
    def calc(self):
        r = {}
        start = self.game.started_date
        today = constants.pacific.localize(datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
        days = (today-start).days
        r['turn'] = days
        r['month'] = constants.months[days%6]
        r['year'] = days//6+1
        r['cp_avail'] = self.ll.cp-sum(b.cost_cp() for b in self.battalions.all())
        r['attack'] = (1+self.ll.level/10)*sum(b.attack() for b in self.battalions.all())
        r['defense'] = (1+self.ll.level/10)*sum(b.defense() for b in self.battalions.all())
        r['oversee'] = sum(b.oversee() for b in self.battalions.all())
        r['work_xp'] = int(sum(b.work_xp() for b in self.battalions.all()))
        gold_mult = max(1,2-(sum(b.count for b in self.battalions.all())/r['oversee']) if r['oversee']>0 else 1)
        r['work_gold'] = int(gold_mult*sum(b.work_gold() for b in self.battalions.all()))
        #payday variable can also add +100 gold, but doesn't show up anywhere?
        return r
        
    def is_protected(self):
        ap_sum = self.logs.aggregate(Sum('action_points'))['action_points__sum']
        if not ap_sum or ap_sum < 3:
            return True
        return False
        
    def avail_action_points(self):
        today = datetime.datetime.now().date()
        ap_sum = self.logs.filter(date__gte=today).aggregate(Sum('action_points'))['action_points__sum']
        return max(0,constants.ACTION_POINTS_PER_DAY-(ap_sum if ap_sum else 0))
        
    def calc_score(self):
        calc = self.calc()
        return int(100*self.ll.level + 80*math.log(max(1,calc['attack'])) + 60*math.log(max(1,calc['defense'])))
        
    def score_rank(self):
        return self.game.player_set.filter(static_score__gt=self.static_score).count()+1
    
    def up_opt_ll(self):
        try:
            return LeaderLevel.objects.get(level=self.ll.level+1, cost_xp__lte=self.xp)
        except ObjectDoesNotExist:
            return None
        
    def up_opts_structure(self):
        q = Structure.objects.exclude(cost_gold__gt=self.gold)
        q = q.exclude(cost_xp__gt=self.xp)
        q = q.exclude(pk__in=self.structures.values_list('pk'))
        q = q.filter(tech_req__isnull=True) | q.filter(tech_req__in=self.technologies.values_list('pk'))
        q = q.filter(struct_req__isnull=True) | q.filter(struct_req__in=self.structures.values_list('pk'))
        return q
        
    def up_opts_technology(self):
        q = Technology.objects.exclude(cost_xp__gt=self.xp)
        q = q.exclude(min_ll__gt=self.ll.level)
        q = q.exclude(pk__in=self.technologies.values_list('pk'))
        q = q.exclude(pk__in=[t.pk for t in q if t.prereq.exclude(pk__in=self.technologies.values_list('pk')).count()])
        return q
    
        
class Battalion(models.Model):
    player = models.ForeignKey(Player, models.CASCADE, related_name='battalions')
    battalion_number = models.PositiveSmallIntegerField(default=1)
    creature = models.ForeignKey(Creature, models.PROTECT, null=True, blank=True)
    count = models.PositiveSmallIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    weapon_base = models.ForeignKey(WeaponBase, models.PROTECT, null=True, blank=True)
    weapon_material = models.ForeignKey(WeaponMaterial, models.PROTECT, null=True, blank=True)
    
    class Meta:
        unique_together = ('player', 'battalion_number',)
        ordering = ['battalion_number']
        
    def __str__(self):
        return 'Battalion {0}'.format(self.battalion_number)
        
    def cost_cp(self):
        return self.count*self.creature.cost_cp if self.creature else 0
    
    def work_gold(self):
        return self.count*self.creature.work_gold if self.creature else 0
        
    def work_xp(self):
        return self.count*self.creature.work_xp if self.creature else 0
        
    def oversee(self):
        return self.count*self.creature.oversee if self.creature else 0
        
    def attack(self):
        v = (1+self.level/10)*self.count*self.creature.attack if self.creature else 0
        if self.weapon_base and self.weapon_material:
            v *= max(1,self.weapon_base.attack_mult*self.weapon_material.attack_mult)
        return v
    
    def defense(self):
        v = (1+self.level/10)*self.count*self.creature.defense if self.creature else 0
        if self.weapon_material:
            v *= max(1,self.weapon_material.armor)
        return v
        
    def training_cost_xp_ea(self):
        return constants.BATTALION_TRAINING_XP_COST
        
    def cost_gold(self, creature):
        unit_cost = creature.cost_gold
        if self.weapon_base and self.weapon_material:
            unit_cost += self.weapon_base.cost_gold*self.weapon_material.cost_mult
        return unit_cost
        
    def cost_xp(self):
        return self.training_cost_xp_ea()*(self.level-1)
        
    def max_hire(self, creature):
        max_gold = self.player.gold // self.cost_gold(creature)
        max_xp = self.player.xp // self.cost_xp() if self.cost_xp() else 10**6
        max_cp = self.player.calc()['cp_avail'] // creature.cost_cp
        return min(max_gold,max_xp,max_cp)
	
    def refund_gold(self):
        if self.weapon_base and self.weapon_material:
            return self.weapon_base.cost_gold*self.weapon_material.cost_mult
        return 0
        
    def arm_cost(self, weapon_base, weapon_material):
        cur_weapons_gold = 0
        if (self.weapon_base and self.weapon_material):
            cur_weapons_gold = self.weapon_base.cost_gold*self.weapon_material.cost_mult
        return self.count*(weapon_base.cost_gold*weapon_material.cost_mult - cur_weapons_gold)
        
    def up_opts_creature(self):
        q = Creature.objects.exclude(min_ll__gt=self.player.ll.level)
        if self.count > 0 and self.creature:
            q = q.filter(pk=self.creature.pk)
        return q
        
    def up_opt_level(self):
        if self.count > 0 and self.level < constants.MAX_BATTALION_LEVEL:
            if self.player.structures.filter(name='Training Grounds').count():
                return self.level+1
        return None
        
    def up_opts_weapon_base(self):
        if self.count <= 0:
            return []
        q = WeaponBase.objects.all()
        q = q.filter(tech_req__isnull=True) | q.filter(tech_req__in=self.player.technologies.values_list('pk'))
        q = q.filter(struct_req__isnull=True) | q.filter(struct_req__in=self.player.structures.values_list('pk'))
        return q
    
    def up_opts_weapon_material(self):
        if self.count <= 0:
            return []
        q = WeaponMaterial.objects.all()
        q = q.filter(tech_req__isnull=True) | q.filter(tech_req__in=self.player.technologies.values_list('pk'))
        q = q.filter(struct_req__isnull=True) | q.filter(struct_req__in=self.player.structures.values_list('pk'))
        return q


class PlayerLog(models.Model):
    ACTIONS = (
        ('work','Work'),
        ('spy','Spy'),
        ('attack','Attack'),
        ('spied-on','Spied on'),
        ('was-attacked','Was Attacked'),
        ('interest','Interest Paid'),
    )
    player = models.ForeignKey(Player, models.PROTECT, related_name='logs')
    target_player = models.ForeignKey(Player, models.PROTECT, blank=True, null=True, related_name='targeted_logs')
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)
    action_points = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=True)
    json_data = models.TextField(blank=True) #for json_data, use json.dumps(pyvar) or pyvar = json.loads(self.json_data)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return '{0} action "{1}" target {2}'.format(self.player.character_name, self.action, self.target_player.character_name if self.target_player else None)



    
