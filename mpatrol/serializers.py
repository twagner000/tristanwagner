from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from . import models


class BriefCreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Creature 
        fields = ('id', 'name', 'cost_cp', 'cost_gold')


class CreatureSerializer(BriefCreatureSerializer):
    class Meta(BriefCreatureSerializer.Meta):
        fields = BriefCreatureSerializer.Meta.fields + ('pk', 'name', 'cost_cp', 'cost_gold', 'plural_name', 'min_ll', 'attack', 'defense', 'work_gold', 'work_xp', 'oversee')


class BriefTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Technology
        fields = ('id', 'name', 'cost_xp')
        

class TechnologySerializer(BriefTechnologySerializer):
    prereq = BriefTechnologySerializer(many=True)
    class Meta(BriefTechnologySerializer.Meta):
        fields = BriefTechnologySerializer.Meta.fields + ('min_ll', 'prereq')
        
        
class BriefStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Structure
        fields = ('id', 'name', 'cost_gold', 'cost_xp')
        

class StructureSerializer(BriefStructureSerializer):
    tech_req = BriefTechnologySerializer()
    struct_req = BriefStructureSerializer()
    class Meta(BriefStructureSerializer.Meta):
        fields = BriefStructureSerializer.Meta.fields + ('tech_req', 'struct_req', 'effects')
        
        
class BriefLeaderLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeaderLevel
        fields = ('id', 'level', 'cost_xp')
        
        
class LeaderLevelSerializer(BriefLeaderLevelSerializer):
    enabled_creatures = BriefCreatureSerializer(read_only=True, many=True)
    class Meta(BriefLeaderLevelSerializer.Meta):
        fields = BriefLeaderLevelSerializer.Meta.fields + ('life', 'cp', 'enabled_creatures')
        
        
class BriefWeaponBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeaponBase
        fields = ('id', 'name', 'cost_gold')
        
        
class WeaponBaseSerializer(BriefWeaponBaseSerializer):
    class Meta(BriefWeaponBaseSerializer.Meta):
        fields = BriefWeaponBaseSerializer.Meta.fields + ('tech_req', 'struct_req', 'attack_mult')


class BriefWeaponMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeaponMaterial
        fields = ('id', 'name', 'cost_mult')


class WeaponMaterialSerializer(BriefWeaponMaterialSerializer):
    class Meta(BriefWeaponMaterialSerializer.Meta):
        fields = BriefWeaponMaterialSerializer.Meta.fields + ('tech_req', 'struct_req', 'attack_mult', 'armor')
        

class BattalionLevelSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    cost_xp_ea = serializers.IntegerField()

    
class BriefBattalionSerializer(serializers.ModelSerializer):
    creature = BriefCreatureSerializer()
    weapon_base = BriefWeaponBaseSerializer()
    weapon_material = BriefWeaponMaterialSerializer()
    
    class Meta:
        model = models.Battalion
        fields = ('id', 'player', 'battalion_number', 'creature', 'count', 'level', 'weapon_base', 'weapon_material')
                  
                  
class BattalionSerializer(BriefBattalionSerializer):
    up_opt_level = BattalionLevelSerializer()
    up_opts_creature = BriefCreatureSerializer(many=True)
    up_opts_weapon_base = BriefWeaponBaseSerializer(many=True)
    up_opts_weapon_material = BriefWeaponMaterialSerializer(many=True)
    
    class Meta(BriefBattalionSerializer.Meta):
        fields = BriefBattalionSerializer.Meta.fields + ('training_cost_xp_ea', 'up_opts_creature', 'up_opt_level', 'up_opts_weapon_base', 'up_opts_weapon_material')
        

class BriefGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Game
        fields = ('id', 'name')
        
        
class PlayerUpgradeSerializer(serializers.ModelSerializer):
    UPGRADES = ('leaderlevel', 'structure', 'technology')
    
    upgrade_type = serializers.ChoiceField(UPGRADES, write_only=True)
    upgrade_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = models.Player
        fields = ('id', 'upgrade_type', 'upgrade_id')
    
    def validate(self, data):
        print('data at serializer validator: {0}'.format(data))
        if data['upgrade_type'] == 'leaderlevel':
            data['upgrade_obj'] = self.instance.up_opt_ll()
            if not data['upgrade_obj'] or data['upgrade_obj'].id != data['upgrade_id']:
                raise serializers.ValidationError("invalid upgrade_id")
        try:
            if data['upgrade_type'] == 'structure':
                data['upgrade_obj'] = self.instance.up_opts_structure().get(id=data['upgrade_id'])
            if data['upgrade_type'] == 'technology':
                data['upgrade_obj'] = self.instance.up_opts_technology().get(id=data['upgrade_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("invalid upgrade_id")
        return data
        
        
class PlayerSerializer(serializers.ModelSerializer):
    game = BriefGameSerializer()
    ll = LeaderLevelSerializer()
    technologies = BriefTechnologySerializer(many=True)
    structures = BriefStructureSerializer(many=True)
    battalions = BriefBattalionSerializer(many=True)
    up_opt_ll = BriefLeaderLevelSerializer()
    up_opts_structure = BriefStructureSerializer(many=True)
    up_opts_technology = BriefTechnologySerializer(many=True)
    
    class Meta:
        model = models.Player
        fields = ('id', 'game', 'character_name', 'll', 'gold', 'xp',
                  'technologies', 'structures', 'battalions', 'calc',
                  'up_opt_ll', 'up_opts_structure', 'up_opts_technology')