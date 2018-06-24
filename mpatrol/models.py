from django.db import models
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
import collections
from datetime import datetime

from . import constants

class Game(models.Model):
    name = models.CharField(blank=True, null=True, max_length=200)
    started_date = models.DateTimeField(auto_now_add=True, editable=True)
    #started_date.editable=True #for testing only
    ended_date = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return '{1} (started {0:%m}/{0:%d}/{0:%y})'.format(self.started_date, self.name)
        
    
class LeaderLevel(models.Model):
    level = models.PositiveSmallIntegerField(unique=True)
    life = models.PositiveIntegerField(default=0)
    cp = models.PositiveIntegerField(default=0)
    xp_cost = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['level']
        
    def __str__(self):
        return str(self.level)
        
    def enabled_creatures(self):
        return Creature.objects.filter(min_ll=self.level)
        
    @staticmethod
    def base_rules():
        LEADER_LEVELS = collections.OrderedDict([
            (1,collections.OrderedDict([('life',20),('cp',5),('xp_cost',0)])),
            (2,collections.OrderedDict([('life',30),('cp',10),('xp_cost',100)])),
            (3,collections.OrderedDict([('life',40),('cp',20),('xp_cost',200)])),
            (4,collections.OrderedDict([('life',50),('cp',50),('xp_cost',500)])),
            (5,collections.OrderedDict([('life',100),('cp',100),('xp_cost',1000)])),
            (6,collections.OrderedDict([('life',200),('cp',200),('xp_cost',2000)])),
            (7,collections.OrderedDict([('life',300),('cp',300),('xp_cost',3000)])),
            (8,collections.OrderedDict([('life',400),('cp',400),('xp_cost',4000)])),
            (9,collections.OrderedDict([('life',500),('cp',500),('xp_cost',5000)])),
            (10,collections.OrderedDict([('life',1000),('cp',1000),('xp_cost',10000)])),
            (11,collections.OrderedDict([('life',2000),('cp',2000),('xp_cost',20000)])),
            (12,collections.OrderedDict([('life',4000),('cp',4000),('xp_cost',40000)])),
            (13,collections.OrderedDict([('life',8000),('cp',8000),('xp_cost',80000)])),
            (14,collections.OrderedDict([('life',16000),('cp',16000),('xp_cost',160000)])),
            (15,collections.OrderedDict([('life',32000),('cp',32000),('xp_cost',320000)]))
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
    level = models.PositiveSmallIntegerField(default=1) #not leader level
    cost_xp = models.PositiveSmallIntegerField(default=100)
    prereq = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name='Prerequisite')
    
    class Meta:
        ordering = ['level','cost_xp','name']
        
    def __str__(self):
        return self.name
        
    def prereq_names(self):
        return self.prereq.values_list('name', flat=True)
        
    @staticmethod
    def base_rules():
        TECHS = collections.OrderedDict([
            ('Bronze Working',collections.OrderedDict([('level',1),('cost',100)])),
            ('Woodworking',collections.OrderedDict([('level',1),('cost',100)])),
            ('Currency',collections.OrderedDict([('level',2),('cost',200)])),
            ('Iron Working',collections.OrderedDict([('level',2),('cost',200)])),
            ('Carpentry',collections.OrderedDict([('level',2),('cost',200)])),
            ('Writing',collections.OrderedDict([('level',2),('cost',200)])),
            ('Trade',collections.OrderedDict([('level',3),('cost',500)])),
            ('Masonry',collections.OrderedDict([('level',4),('cost',1000)])),
            ('Weaving',collections.OrderedDict([('level',4),('cost',1000)])),
            ('Map Making',collections.OrderedDict([('level',4),('cost',1000)]))
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
            ('Armor',collections.OrderedDict([('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',0),('cost_gold',1)]))
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
            ('Leather',collections.OrderedDict([('tech_req',Technology.objects.get(name='Bronze Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',0),('cost_mult',100),('armor',5)])),
            ('Chainmail',collections.OrderedDict([('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',0),('cost_mult',200),('armor',8)])),
            ('Plate',collections.OrderedDict([('tech_req',Technology.objects.get(name='Iron Working')),('struct_req',Structure.objects.get(name='Armory')),('attack_mult',0),('cost_mult',300),('armor',10)]))
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
    last_action_date = models.DateTimeField(blank=True, null=True)
    
    ll = models.ForeignKey(LeaderLevel, models.PROTECT, verbose_name='Leader Level')
    gold = models.PositiveIntegerField(default=100)
    xp = models.PositiveIntegerField(default=0, verbose_name='Experience')
    technologies = models.ManyToManyField(Technology, blank=True)
    structures = models.ManyToManyField(Structure, blank=True)
    
    #medals, missions_completed, Special Abilities, Allies (Up to 10)
    
    class Meta:
        unique_together = ('game', 'user',)
        
    def __str__(self):
        return str(self.user)
        
    def save(self, *args, **kwargs):
        try:
            self.ll
        except:
            self.ll = LeaderLevel.objects.get(level=1)
        super().save(*args, **kwargs)
    
    def calc(self):
        r = {}
        start = self.game.started_date.astimezone(constants.pacific).date()
        today = datetime.now().astimezone(constants.pacific).date()
        last_action = self.last_action_date.astimezone(constants.pacific).date() if self.last_action_date else None
        days = (today-start).days
        r['turn'] = days
        r['month'] = constants.months[days%6]
        r['year'] = days//6+1
        r['action_taken'] = last_action==today
        r['cp_avail'] = self.ll.cp-sum(b.cost_cp() for b in self.battalions.all())
        r['attack'] = (1+self.ll.level/10)*sum(b.attack() for b in self.battalions.all())
        r['defense'] = (1+self.ll.level/10)*sum(b.defense() for b in self.battalions.all())
        r['oversee'] = sum(b.oversee() for b in self.battalions.all())
        r['work_xp'] = sum(b.work_xp() for b in self.battalions.all())
        gold_mult = max(1,2-(sum(b.count for b in self.battalions.all())/r['oversee']) if r['oversee']>0 else 1)
        r['work_gold'] = gold_mult*sum(b.work_gold() for b in self.battalions.all())
        #payday variable can also add +100 gold, but doesn't show up anywhere?
        return r
        
    def battles_fought(self):
        return self.attacker_set.all() | self.defender_set.all()
        
    def unread_message_count(self):
        return self.recipient_set.filter(unread=True).count()
        
    def ll_upgrade(self):
        return LeaderLevel.objects.filter(level=self.ll.level+1).first()
        
    def structure_upgrade(self):
        q = Structure.objects.exclude(cost_gold__gt=self.gold)
        q = q.exclude(cost_xp__gt=self.xp)
        q = q.exclude(pk__in=self.structures.values_list('pk'))
        q = q.filter(tech_req__isnull=True) | q.filter(tech_req__in=self.technologies.values_list('pk'))
        q = q.filter(struct_req__isnull=True) | q.filter(struct_req__in=self.structures.values_list('pk'))
        return q
        
    def technology_upgrade(self):
        q = Technology.objects.exclude(cost_xp__gt=self.xp)
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
    

class Message(models.Model):
    #see messages.e.txt
    sender = models.ForeignKey(Player, models.PROTECT, related_name='sender_set', null=True)
    recipient = models.ForeignKey(Player, models.PROTECT, related_name='recipient_set')
    sent_date = models.DateTimeField(auto_now_add=True)
    subject = models.TextField()
    message = models.TextField(blank=True)
    unread = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-sent_date']
    
    def __str__(self):
        return 'Message "{0}" from {1} to {2}'.format(self.subject, self.sender, self.recipient)
    
    
class Battle(models.Model):
    attacker = models.ForeignKey(Player, models.PROTECT, related_name='attacker_set')
    defender = models.ForeignKey(Player, models.PROTECT, related_name='defender_set')
    battle_date = models.DateTimeField(auto_now_add=True)
    successful_attack = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-battle_date']
    
    def __str__(self):
        return 'Battle {0} attacked {1} on {2}'.format(self.attacker, self.defender, self.battle_date)



    
