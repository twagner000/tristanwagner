import collections

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
    
LEADER_LEVEL_COLUMNS = collections.OrderedDict([
    ('life','Life'),
    ('cp','Creature Points'),
    ('xp_cost','Experience Cost')
    ])
    
CREATURES = collections.OrderedDict([
    ('Shrew',collections.OrderedDict([('pluralname','Shrews'),('ll',1),('attack',1),('defense',1),('cost_cp',1),('cost_gold',20),('work_gold',5),('work_xp',1),('oversee',0)])),
    ('Vole',collections.OrderedDict([('pluralname','Voles'),('ll',1),('attack',0),('defense',2),('cost_cp',1),('cost_gold',20),('work_gold',5),('work_xp',10),('oversee',0)])),
    ('Mouse',collections.OrderedDict([('pluralname','Mice'),('ll',1),('attack',2),('defense',1),('cost_cp',1),('cost_gold',40),('work_gold',10),('work_xp',15),('oversee',0)])),
    ('Hedgehog',collections.OrderedDict([('pluralname','Hedgehogs'),('ll',2),('attack',2),('defense',3),('cost_cp',2),('cost_gold',50),('work_gold',15),('work_xp',15),('oversee',0)])),
    ('Squirrel',collections.OrderedDict([('pluralname','Squirrels'),('ll',2),('attack',3),('defense',2),('cost_cp',2),('cost_gold',50),('work_gold',20),('work_xp',20),('oversee',0)])),
    ('Otter',collections.OrderedDict([('pluralname','Otters'),('ll',3),('attack',4),('defense',2),('cost_cp',3),('cost_gold',75),('work_gold',40),('work_xp',40),('oversee',0)])),
    ('Hare',collections.OrderedDict([('pluralname','Hares'),('ll',4),('attack',4),('defense',4),('cost_cp',4),('cost_gold',85),('work_gold',50),('work_xp',60),('oversee',0)])),
    ('Sparrow',collections.OrderedDict([('pluralname','Sparrows'),('ll',4),('attack',6),('defense',2),('cost_cp',4),('cost_gold',100),('work_gold',20),('work_xp',70),('oversee',5)])),
    ('Owl',collections.OrderedDict([('pluralname','Owls'),('ll',5),('attack',8),('defense',4),('cost_cp',6),('cost_gold',125),('work_gold',20),('work_xp',70),('oversee',10)])),
    ('Heron',collections.OrderedDict([('pluralname','Herons'),('ll',6),('attack',10),('defense',6),('cost_cp',8),('cost_gold',175),('work_gold',30),('work_xp',50),('oversee',15)])),
    ('Badger',collections.OrderedDict([('pluralname','Badgers'),('ll',6),('attack',12),('defense',10),('cost_cp',10),('cost_gold',200),('work_gold',80),('work_xp',80),('oversee',0)]))
    ])

CREATURE_COLUMNS = collections.OrderedDict([
    ('ll','Min Leader Level'),
    ('attack','Attack'),
    ('defense','Defense'),
    ('cost_cp','Cost in Creature Points'),
    ('cost_gold','Cost in Gold'),
    ('work_gold','Gold from Working'),
    ('work_xp','Experience from Working'),
    ('oversee','Overseeing Capability')
    ])
    
STRUCTURES = collections.OrderedDict([
    ('Armory',collections.OrderedDict([('cost_gold',300),('cost_xp',500),('tech_req','Bronze Working'),('struct_req',None),('effects','Allows construction of armor')])),
    ('Training Grounds',collections.OrderedDict([('cost_gold',200),('cost_xp',300),('tech_req','Bronze Working'),('struct_req',None),('effects','Allows training of battalions')])),
    ('Workshop',collections.OrderedDict([('cost_gold',200),('cost_xp',300),('tech_req','Woodworking'),('struct_req',None),('effects','Allows construction of Level 1 Weapons')])),
    ('Blacksmith',collections.OrderedDict([('cost_gold',700),('cost_xp',1000),('tech_req','Iron Working'),('struct_req','Workshop'),('effects','Allows construction of Level 2 Weapons')])),
    ('Treasury',collections.OrderedDict([('cost_gold',500),('cost_xp',100),('tech_req','Currency'),('struct_req',None),('effects','5% Interest on gold every year')])),
    ('Library',collections.OrderedDict([('cost_gold',700),('cost_xp',300),('tech_req','Writing'),('struct_req',None),('effects','10% Interest on experience every year')])),
    ('Marketplace',collections.OrderedDict([('cost_gold',1000),('cost_xp',300),('tech_req','Trade'),('struct_req','Treasury'),('effects','10% Interest on gold every year (cumulative with Treasury\'s 5% for a total of 15%)')])),
    ])
    
TECHS = collections.OrderedDict([
    ('Bronze Working',collections.OrderedDict([('level',1),('cost',100),('tech_req',None)])),
    ('Woodworking',collections.OrderedDict([('level',1),('cost',100),('tech_req',None)])),
    ('Currency',collections.OrderedDict([('level',2),('cost',200),('tech_req',('Bronze Working',))])),
    ('Iron Working',collections.OrderedDict([('level',2),('cost',200),('tech_req',('Bronze Working', 'Woodworking'))])),
    ('Carpentry',collections.OrderedDict([('level',2),('cost',200),('tech_req',('Woodworking',))])),
    ('Writing',collections.OrderedDict([('level',2),('cost',200),('tech_req',None)])),
    ('Trade',collections.OrderedDict([('level',3),('cost',500),('tech_req',('Currency', 'Writing'))])),
    ('Masonry',collections.OrderedDict([('level',4),('cost',1000),('tech_req',('Iron Working', 'Carpentry', 'Trade'))])),
    ('Weaving',collections.OrderedDict([('level',4),('cost',1000),('tech_req',('Trade',))])),
    ('Map Making',collections.OrderedDict([('level',4),('cost',1000),('tech_req',('Trade',))]))
    ])
    
WEAPON_BASES = collections.OrderedDict([
    ('Slingshot',collections.OrderedDict([('tech_req','Woodworking'),('struct_req','Workshop'),('attack_mult',1.5),('cost',10)])),
    ('Dagger',collections.OrderedDict([('tech_req','Bronze Working'),('struct_req','Workshop'),('attack_mult',2),('cost',20)])),
    ('Bow',collections.OrderedDict([('tech_req','Woodworking'),('struct_req','Workshop'),('attack_mult',2.5),('cost',30)])),
    ('Javelin',collections.OrderedDict([('tech_req','Carpentry'),('struct_req','Blacksmith'),('attack_mult',3),('cost',40)])),
    ('Longbow & Arrows',collections.OrderedDict([('tech_req','Carpentry'),('struct_req','Blacksmith'),('attack_mult',4),('cost',50)])),
    ('Sword',collections.OrderedDict([('tech_req','Iron Working'),('struct_req','Blacksmith'),('attack_mult',5),('cost',60)])),
    ('Armor',collections.OrderedDict([('tech_req','Bronze Working'),('struct_req','Armory'),('attack_mult',0),('cost',1)]))
    ])
    
WEAPON_MATERIALS = collections.OrderedDict([
    ('Wood',collections.OrderedDict([('tech_req','Woodworking'),('struct_req','Workshop'),('attack_mult',1),('cost_mult',1),('armor',0)])),
    ('Bronze',collections.OrderedDict([('tech_req','Bronze Working'),('struct_req','Workshop'),('attack_mult',2),('cost_mult',1.5),('armor',2)])),
    ('Iron',collections.OrderedDict([('tech_req','Iron Working'),('struct_req','Blacksmith'),('attack_mult',3),('cost_mult',2),('armor',4)])),
    ('Leather',collections.OrderedDict([('tech_req','Bronze Working'),('struct_req','Armory'),('attack_mult',0),('cost_mult',100),('armor',5)])),
    ('Chainmail',collections.OrderedDict([('tech_req','Iron Working'),('struct_req','Armory'),('attack_mult',0),('cost_mult',200),('armor',8)])),
    ('Plate',collections.OrderedDict([('tech_req','Iron Working'),('struct_req','Armory'),('attack_mult',0),('cost_mult',300),('armor',10)]))
    ])