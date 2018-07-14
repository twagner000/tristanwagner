import datetime
import collections
from pytz import timezone

from . import models

pacific = timezone('US/Pacific')
months = {0:'January',1:'March',2:'May',3:'July',4:'September',5:'November'}

MAX_BATTALION_LEVEL = 15
BATTALION_TRAINING_XP_COST = 10

refresh_score_timedelta = datetime.timedelta(minutes=1)

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
        r,created = models.LeaderLevel.objects.get_or_create(level=k)
        for k2,v2 in v.items():
            setattr(r,k2,v2)
        r.save()
        
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
        r,created = models.Creature.objects.get_or_create(name=k)
        for k2,v2 in v.items():
            setattr(r,k2,v2)
        r.save()
    
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
        r,created = models.Technology.objects.get_or_create(name=k)
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
        models.Technology.objects.get(name=t).prereq.add(models.Technology.objects.get(name=p))
        
    STRUCTURES = collections.OrderedDict([
        ('Armory',collections.OrderedDict([('cost_gold',300),('cost_xp',500),('tech_req',models.Technology.objects.get(name='Bronze Working')),('struct_req',None),('effects','Allows construction of armor')])),
        ('Training Grounds',collections.OrderedDict([('cost_gold',200),('cost_xp',300),('tech_req',models.Technology.objects.get(name='Bronze Working')),('struct_req',None),('effects','Allows training of battalions')])),
        ('Workshop',collections.OrderedDict([('cost_gold',200),('cost_xp',300),('tech_req',models.Technology.objects.get(name='Woodworking')),('struct_req',None),('effects','Allows construction of basic weapons')])),
        ('Blacksmith',collections.OrderedDict([('cost_gold',700),('cost_xp',1000),('tech_req',models.Technology.objects.get(name='Iron Working')),('struct_req',None),('effects','Allows construction of advanced weapons')])),
        ('Treasury',collections.OrderedDict([('cost_gold',500),('cost_xp',100),('tech_req',models.Technology.objects.get(name='Currency')),('struct_req',None),('effects','5% interest on gold every year')])),
        ('Library',collections.OrderedDict([('cost_gold',700),('cost_xp',300),('tech_req',models.Technology.objects.get(name='Writing')),('struct_req',None),('effects','10% interest on experience every year')])),
        ('Marketplace',collections.OrderedDict([('cost_gold',1000),('cost_xp',300),('tech_req',models.Technology.objects.get(name='Trade')),('struct_req',None),('effects','10% interest on gold every year (stacks with Treasury)')])),
        ])
    for k,v in STRUCTURES.items():
        r,created = models.Structure.objects.get_or_create(name=k)
        for k2,v2 in v.items():
            setattr(r,k2,v2)
        r.save()
    r = models.Structure.objects.get(name='Blacksmith')
    r.struct_req = models.Structure.objects.get(name='Workshop')
    r.save()
    r = models.Structure.objects.get(name='Marketplace')
    r.struct_req = models.Structure.objects.get(name='Treasury')
    r.save()
    
    WEAPON_BASES = collections.OrderedDict([
        ('Slingshot',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Woodworking')),('struct_req',models.Structure.objects.get(name='Workshop')),('attack_mult',1.5),('cost_gold',10)])),
        ('Dagger',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Bronze Working')),('struct_req',models.Structure.objects.get(name='Workshop')),('attack_mult',2),('cost_gold',20)])),
        ('Bow',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Woodworking')),('struct_req',models.Structure.objects.get(name='Workshop')),('attack_mult',2.5),('cost_gold',30)])),
        ('Javelin',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Carpentry')),('struct_req',models.Structure.objects.get(name='Blacksmith')),('attack_mult',3),('cost_gold',40)])),
        ('Longbow & Arrows',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Carpentry')),('struct_req',models.Structure.objects.get(name='Blacksmith')),('attack_mult',4),('cost_gold',50)])),
        ('Sword',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Iron Working')),('struct_req',models.Structure.objects.get(name='Blacksmith')),('attack_mult',5),('cost_gold',60)])),
        ('Armor',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Bronze Working')),('struct_req',models.Structure.objects.get(name='Armory')),('attack_mult',1),('cost_gold',10)]))
        ])
    for k,v in WEAPON_BASES.items():
        r,created = models.WeaponBase.objects.get_or_create(name=k)
        for k2,v2 in v.items():
            setattr(r,k2,v2)
        r.save()
    
    WEAPON_MATERIALS = collections.OrderedDict([
        ('Wood',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Woodworking')),('struct_req',models.Structure.objects.get(name='Workshop')),('attack_mult',1),('cost_mult',1),('armor',0)])),
        ('Bronze',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Bronze Working')),('struct_req',models.Structure.objects.get(name='Workshop')),('attack_mult',2),('cost_mult',1.5),('armor',2)])),
        ('Iron',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Iron Working')),('struct_req',models.Structure.objects.get(name='Blacksmith')),('attack_mult',3),('cost_mult',2),('armor',4)])),
        ('Leather',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Bronze Working')),('struct_req',models.Structure.objects.get(name='Armory')),('attack_mult',1),('cost_mult',10),('armor',5)])),
        ('Chainmail',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Iron Working')),('struct_req',models.Structure.objects.get(name='Armory')),('attack_mult',1),('cost_mult',20),('armor',8)])),
        ('Plate',collections.OrderedDict([('tech_req',models.Technology.objects.get(name='Iron Working')),('struct_req',models.Structure.objects.get(name='Armory')),('attack_mult',1),('cost_mult',30),('armor',10)]))
        ])
    for k,v in WEAPON_MATERIALS.items():
        r,created = models.WeaponMaterial.objects.get_or_create(name=k)
        for k2,v2 in v.items():
            setattr(r,k2,v2)
        r.save()  