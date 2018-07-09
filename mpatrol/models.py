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
    started_date = models.DateTimeField(auto_now_add=True) #, editable=True
    #started_date.editable=True #for testing only
    ended_date = models.DateTimeField(blank=True,null=True)
    
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
        
    @staticmethod
    def base_rules():
        LEADER_LEVELS = collections.OrderedDict([
            (1,collections.OrderedDict([('life',20),('cp',5),('cost_xp',0)])),
            (2,collections.OrderedDict([('life',30),('cp',10),('cost_xp',100)])),
            (3,collections.OrderedDict([('life',40),('cp',20),('cost_xp',200)])),
            (4,collections.OrderedDict([('life',50),('cp',50),('cost_xp',500)])),
            (5,collections.OrderedDict([('life',100),('cp',100),('cost_xp',1000)])),
            (6,collections.OrderedDict([('life',200),('cp',200),('cost_xp',2000)])),
            (7,collections.OrderedDict([('life',300),('cp',300),('cost_xp',3000)])),
            (8,collections.OrderedDict([('life',400),('cp',400),('cost_xp',4000)])),
            (9,collections.OrderedDict([('life',500),('cp',500),('cost_xp',5000)])),
            (10,collections.OrderedDict([('life',1000),('cp',1000),('cost_xp',10000)])),
            (11,collections.OrderedDict([('life',2000),('cp',2000),('cost_xp',20000)])),
            (12,collections.OrderedDict([('life',4000),('cp',4000),('cost_xp',40000)])),
            (13,collections.OrderedDict([('life',8000),('cp',8000),('cost_xp',80000)])),
            (14,collections.OrderedDict([('life',16000),('cp',16000),('cost_xp',160000)])),
            (15,collections.OrderedDict([('life',32000),('cp',32000),('cost_xp',320000)]))
            ])
        for k,v in LEADER_LEVELS.items():
            r,created = LeaderLevel.objects.get_or_create(level=k)
            for k2,v2 in v.items():
                setattr(r,k2,v2)
            r.save()
        
    
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
        
    @staticmethod
    def base_rules():
        CREATURES = collections.OrderedDict([
            ('Shrew',collections.OrderedDict([('plural_name','Shrews'),('min_ll',1),('attack',1),('defense',1),('cost_cp',1),('cost_gold',20),('work_gold',5),('work_xp',1),('oversee',0)])),
            ('Vole',collections.OrderedDict([('plural_name','Voles'),('min_ll',1),('attack',0),('defense',2),('cost_cp',1),('cost_gold',20),('work_gold',5),('work_xp',10),('oversee',0)])),
            ('Mouse',collections.OrderedDict([('plural_name','Mice'),('min_ll',1),('attack',2),('defense',1),('cost_cp',1),('cost_gold',40),('work_gold',10),('work_xp',15),('oversee',0)])),
            ('Hedgehog',collections.OrderedDict([('plural_name','Hedgehogs'),('min_ll',2),('attack',2),('defense',3),('cost_cp',2),('cost_gold',50),('work_gold',15),('work_xp',15),('oversee',0)])),
            ('Squirrel',collections.OrderedDict([('plural_name','Squirrels'),('min_ll',2),('attack',3),('defense',2),('cost_cp',2),('cost_gold',50),('work_gold',20),('work_xp',20),('oversee',0)])),
            ('Otter',collections.OrderedDict([('plural_name','Otters'),('min_ll',3),('attack',4),('defense',2),('cost_cp',3),('cost_gold',75),('work_gold',40),('work_xp',40),('oversee',0)])),
            ('Hare',collections.OrderedDict([('plural_name','Hares'),('min_ll',4),('attack',4),('defense',4),('cost_cp',4),('cost_gold',85),('work_gold',50),('work_xp',60),('oversee',0)])),
            ('Sparrow',collections.OrderedDict([('plural_name','Sparrows'),('min_ll',4),('attack',6),('defense',2),('cost_cp',4),('cost_gold',100),('work_gold',20),('work_xp',70),('oversee',5)])),
            ('Owl',collections.OrderedDict([('plural_name','Owls'),('min_ll',5),('attack',8),('defense',4),('cost_cp',6),('cost_gold',125),('work_gold',20),('work_xp',70),('oversee',10)])),
            ('Heron',collections.OrderedDict([('plural_name','Herons'),('min_ll',6),('attack',10),('defense',6),('cost_cp',8),('cost_gold',175),('work_gold',30),('work_xp',50),('oversee',15)])),
            ('Badger',collections.OrderedDict([('plural_name','Badgers'),('min_ll',6),('attack',12),('defense',10),('cost_cp',10),('cost_gold',200),('work_gold',80),('work_xp',80),('oversee',0)]))
            ])
        for k,v in CREATURES.items():
            r,created = Creature.objects.get_or_create(name=k)
            for k2,v2 in v.items():
                setattr(r,k2,v2)
            r.save()


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
        
    @staticmethod
    def base_rules():
        TECHS = collections.OrderedDict([
            ('Bronze Working',collections.OrderedDict([('min_ll',1),('cost',100)])),
            ('Woodworking',collections.OrderedDict([('min_ll',1),('cost',100)])),
            ('Currency',collections.OrderedDict([('min_ll',2),('cost',200)])),
            ('Iron Working',collections.OrderedDict([('min_ll',2),('cost',200)])),
            ('Carpentry',collections.OrderedDict([('min_ll',2),('cost',200)])),
            ('Writing',collections.OrderedDict([('min_ll',2),('cost',200)])),
            ('Trade',collections.OrderedDict([('min_ll',3),('cost',500)])),
            ('Masonry',collections.OrderedDict([('min_ll',4),('cost',1000)])),
            ('Weaving',collections.OrderedDict([('min_ll',4),('cost',1000)])),
            ('Map Making',collections.OrderedDict([('min_ll',4),('cost',1000)]))
            ])
        for k,v in TECHS.items():
            r,created = Technology.objects.get_or_create(name=k)
            for k2,v2 in v.items():
                setattr(r,k2,v2)
            r.prereq.clear()
            r.save()
        PREREQS = [('Currency','Bronze Working'),
            ('Iron Working','Bronze Working'),
            ('Iron Working','Woodworking'),
            ('Carpentry','Woodworking'),
            ('Trade','Currency'),
            ('Trade','Writing'),
            ('Masonry','Iron Working'),
            ('Masonry','Carpentry'),
            ('Masonry','Trade'),
            ('Weaving','Trade'),
            ('Map Making','Trade')
            ]
        for (t,p) in PREREQS:
            Technology.objects.get(name=t).prereq.add(Technology.objects.get(name=p))


class Structure(models.Model):
    name = models.CharField(unique=True, max_length=50)
    cost_gold = models.PositiveSmallIntegerField(default=100)
    cost_xp = models.PositiveSmallIntegerField(default=100)
    tech_req = models.ForeignKey(Technology, models.PROTECT, null=True, blank=True, verbose_name='Required Technology')
    struct_req = models.ForeignKey('self', models.PROTECT, null=True, blank=True, verbose_name='Required Structure')
    effects = models.TextField(blank=True)
    
    class Meta:
        ordering = ['cost_gold','cost_xp','name']
        
    def __str__(self):
        return self.name
        
    @staticmethod
    def base_rules():
        STRUCTURES = collections.OrderedDict([
            ('Armory',collections.OrderedDict([('cost_gold',300),('cost_xp',500),('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',None),('effects','Allows construction of armor')])),
            ('Training Grounds',collections.OrderedDict([('cost_gold',200),('cost_xp',300),('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',None),('effects','Allows training of battalions')])),
            ('Workshop',collections.OrderedDict([('cost_gold',200),('cost_xp',300),('tech_req',Technology.objects.get(name='Woodworking')),('struct_req',None),('effects','Allows construction of basic weapons')])),
            ('Blacksmith',collections.OrderedDict([('cost_gold',700),('cost_xp',1000),('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',None),('effects','Allows construction of advanced weapons')])),
            ('Treasury',collections.OrderedDict([('cost_gold',500),('cost_xp',100),('tech_req',Technology.objects.get(name='Currency')),('struct_req',None),('effects','5% interest on gold every year')])),
            ('Library',collections.OrderedDict([('cost_gold',700),('cost_xp',300),('tech_req',Technology.objects.get(name='Writing')),('struct_req',None),('effects','10% interest on experience every year')])),
            ('Marketplace',collections.OrderedDict([('cost_gold',1000),('cost_xp',300),('tech_req',Technology.objects.get(name='Trade')),('struct_req',None),('effects','10% interest on gold every year (stacks with Treasury)')])),
            ])
        for k,v in STRUCTURES.items():
            r,created = Structure.objects.get_or_create(name=k)
            for k2,v2 in v.items():
                setattr(r,k2,v2)
            r.save()
        r = Structure.objects.get(name='Blacksmith')
        r.struct_req = Structure.objects.get(name='Workshop')
        r.save()
        r = Structure.objects.get(name='Marketplace')
        r.struct_req = Structure.objects.get(name='Treasury')
        r.save()
            
            
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
        
    @staticmethod
    def base_rules():
        WEAPON_BASES = collections.OrderedDict([
            ('Slingshot',collections.OrderedDict([('tech_req',Technology.objects.get(name='Woodworking')),('struct_req',Structure.objects.get(name='Workshop')),('attack_mult',1.5),('cost_gold',10)])),
            ('Dagger',collections.OrderedDict([('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',Structure.objects.get(name='Workshop')),('attack_mult',2),('cost_gold',20)])),
            ('Bow',collections.OrderedDict([('tech_req',Technology.objects.get(name='Woodworking')),('struct_req',Structure.objects.get(name='Workshop')),('attack_mult',2.5),('cost_gold',30)])),
            ('Javelin',collections.OrderedDict([('tech_req',Technology.objects.get(name='Carpentry')),('struct_req',Structure.objects.get(name='Blacksmith')),('attack_mult',3),('cost_gold',40)])),
            ('Longbow & Arrows',collections.OrderedDict([('tech_req',Technology.objects.get(name='Carpentry')),('struct_req',Structure.objects.get(name='Blacksmith')),('attack_mult',4),('cost_gold',50)])),
            ('Sword',collections.OrderedDict([('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',Structure.objects.get(name='Blacksmith')),('attack_mult',5),('cost_gold',60)])),
            ('Armor',collections.OrderedDict([('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',1),('cost_gold',10)]))
            ])
        for k,v in WEAPON_BASES.items():
            r,created = WeaponBase.objects.get_or_create(name=k)
            for k2,v2 in v.items():
                setattr(r,k2,v2)
            r.save()


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
        
    @staticmethod
    def base_rules():
        WEAPON_MATERIALS = collections.OrderedDict([
            ('Wood',collections.OrderedDict([('tech_req',Technology.objects.get(name='Woodworking')),('struct_req',Structure.objects.get(name='Workshop')),('attack_mult',1),('cost_mult',1),('armor',0)])),
            ('Bronze',collections.OrderedDict([('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',Structure.objects.get(name='Workshop')),('attack_mult',2),('cost_mult',1.5),('armor',2)])),
            ('Iron',collections.OrderedDict([('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',Structure.objects.get(name='Blacksmith')),('attack_mult',3),('cost_mult',2),('armor',4)])),
            ('Leather',collections.OrderedDict([('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',1),('cost_mult',10),('armor',5)])),
            ('Chainmail',collections.OrderedDict([('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',1),('cost_mult',20),('armor',8)])),
            ('Plate',collections.OrderedDict([('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',1),('cost_mult',30),('armor',10)]))
            ])
        for k,v in WEAPON_MATERIALS.items():
            r,created = WeaponMaterial.objects.get_or_create(name=k)
            for k2,v2 in v.items():
                setattr(r,k2,v2)
            r.save()  


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
        start = self.game.started_date.astimezone(constants.pacific).date()
        today = datetime.datetime.now().astimezone(constants.pacific).date()
        days = (today-start).days
        r['turn'] = days
        r['month'] = constants.months[days%6]
        r['year'] = days//6+1
        r['cp_avail'] = self.ll.cp-sum(b.cost_cp() for b in self.battalions.all())
        r['attack'] = (1+self.ll.level/10)*sum(b.attack() for b in self.battalions.all())
        r['defense'] = (1+self.ll.level/10)*sum(b.defense() for b in self.battalions.all())
        r['oversee'] = sum(b.oversee() for b in self.battalions.all())
        r['work_xp'] = sum(b.work_xp() for b in self.battalions.all())
        gold_mult = max(1,2-(sum(b.count for b in self.battalions.all())/r['oversee']) if r['oversee']>0 else 1)
        r['work_gold'] = gold_mult*sum(b.work_gold() for b in self.battalions.all())
        #payday variable can also add +100 gold, but doesn't show up anywhere?
        return r
        
    def is_protected(self):
        ap_sum = self.logs.aggregate(Sum('action_points'))['action_points__sum']
        if not ap_sum or ap_sum < 3:
            return True
        return False
        
    def avail_action_points(self):
        return 1
        today = datetime.datetime.now().astimezone(constants.pacific).date()
        ap_sum = self.logs.filter(date__gte=today).aggregate(Sum('action_points'))['action_points__sum']
        return max(0,1-(ap_sum if ap_sum else 0))
        
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



    
