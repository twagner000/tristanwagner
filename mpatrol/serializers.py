from rest_framework import serializers
from . import models


class BriefCreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Creature 
        fields = ('id', 'name', 'cost_cp', 'cost_gold')


class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Creature 
        fields = ('pk', 'name', 'cost_cp', 'cost_gold', 'plural_name', 'min_ll', 'attack', 'defense', 'work_gold', 'work_xp', 'oversee')
        #depth = 1


class BriefTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technology
        fields = ('id', 'name', 'cost_xp')
        

class TechnologySerializer(serializers.ModelSerializer):
    prereq = BriefTechnologySerializer(many=True)
    class Meta:
        model = models.Technology
        fields = ('id', 'name', 'cost_xp', 'min_ll', 'prereq')
        
        
class BriefStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Structure
        fields = ('id', 'name', 'cost_gold', 'cost_xp')
        

class StructureSerializer(serializers.ModelSerializer):
    tech_req = BriefTechnologySerializer()
    struct_req = BriefStructureSerializer()
    class Meta:
        model = models.Structure
        fields = ('id', 'name', 'cost_gold', 'cost_xp', 'tech_req', 'struct_req', 'effects')
        
        
class BriefLeaderLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderLevel
        fields = ('id', 'level', 'xp_cost')
        
        
class LeaderLevelSerializer(serializers.ModelSerializer):
    enabled_creatures = BriefCreatureSerializer(read_only=True, many=True)
    class Meta:
        model = models.LeaderLevel
        fields = ('id', 'level', 'xp_cost', 'life', 'cp', 'enabled_creatures')
        
        
class BriefWeaponBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeaponBase
        fields = ('id', 'name', 'cost_gold')


class BriefWeaponMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeaponMaterial
        fields = ('id', 'name', 'cost_mult')
        
        
class WeaponBaseSerializer(BriefWeaponBaseSerializer):
    class Meta(BriefWeaponBaseSerializer.Meta):
        fields = BriefWeaponBaseSerializer.Meta.fields + ('tech_req', 'struct_req', 'attack_mult')


class WeaponMaterialSerializer(BriefWeaponMaterialSerializer):
    class Meta(BriefWeaponMaterialSerializer.Meta):
        fields = BriefWeaponMaterialSerializer.Meta.fields + ('tech_req', 'struct_req', 'attack_mult', 'armor')
        

class BattalionLevelSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    cost_xp_ea = serializers.IntegerField()

    
class BattalionSerializer(serializers.ModelSerializer):
    creature = BriefCreatureSerializer()
    weapon_base = BriefWeaponBaseSerializer()
    weapon_material = BriefWeaponMaterialSerializer()
    up_opt_level = BattalionLevelSerializer()
    up_opts_creature = BriefCreatureSerializer(many=True)
    up_opts_weapon_base = BriefWeaponBaseSerializer(many=True)
    up_opts_weapon_material = BriefWeaponMaterialSerializer(many=True)
    
    class Meta:
        model = models.Battalion
        fields = ('id', 'battalion_number', 'creature', 'count', 'level', 'weapon_base', 'weapon_material',
                  'up_opts_creature', 'up_opt_level', 'up_opts_weapon_base', 'up_opts_weapon_material')
        

class BriefGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('id', 'name')
        
        
class PlayerSerializer(serializers.ModelSerializer):
    game = BriefGameSerializer()
    ll = LeaderLevelSerializer()
    technologies = BriefTechnologySerializer(many=True)
    structures = BriefStructureSerializer(many=True)
    battalions = BattalionSerializer(many=True)
    up_opt_ll = BriefLeaderLevelSerializer()
    up_opts_structure = BriefStructureSerializer(many=True)
    up_opts_technology = BriefTechnologySerializer(many=True)
    
    class Meta:
        model = models.Player
        fields = ('id', 'game', 'character_name', 'll', 'gold', 'xp',
                  'technologies', 'structures', 'battalions', 'calc',
                  'up_opt_ll', 'up_opts_structure', 'up_opts_technology')