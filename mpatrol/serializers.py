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
    tech_req = BriefTechnologySerializer()
    struct_req = BriefStructureSerializer()
    
    class Meta(BriefWeaponBaseSerializer.Meta):
        fields = BriefWeaponBaseSerializer.Meta.fields + ('tech_req', 'struct_req', 'attack_mult')


class BriefWeaponMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WeaponMaterial
        fields = ('id', 'name', 'cost_mult')


class WeaponMaterialSerializer(BriefWeaponMaterialSerializer):
    tech_req = BriefTechnologySerializer()
    struct_req = BriefStructureSerializer()
    
    class Meta(BriefWeaponMaterialSerializer.Meta):
        fields = BriefWeaponMaterialSerializer.Meta.fields + ('tech_req', 'struct_req', 'attack_mult', 'armor')

    
class BriefBattalionSerializer(serializers.ModelSerializer):
    creature = BriefCreatureSerializer()
    weapon_base = BriefWeaponBaseSerializer()
    weapon_material = BriefWeaponMaterialSerializer()
    
    class Meta:
        model = models.Battalion
        fields = ('id', 'player', 'battalion_number', 'creature', 'count', 'level', 'weapon_base', 'weapon_material')
                  
                  
class BattalionSerializer(BriefBattalionSerializer):
    up_opt_level = serializers.IntegerField()
    up_opts_creature = BriefCreatureSerializer(many=True)
    up_opts_weapon_base = BriefWeaponBaseSerializer(many=True)
    up_opts_weapon_material = BriefWeaponMaterialSerializer(many=True)
    
    class Meta(BriefBattalionSerializer.Meta):
        fields = BriefBattalionSerializer.Meta.fields + ('training_cost_xp_ea', 'up_opts_creature', 'up_opt_level', 'up_opts_weapon_base', 'up_opts_weapon_material')


class BattalionUpdateSerializer(serializers.ModelSerializer):
    ACTIONS = ('hire','fire','train','arm')
    action = serializers.ChoiceField(ACTIONS, write_only=True)
    creature_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    count_delta = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    level = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    weapon_base_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    weapon_material_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    
    class Meta:
        model = models.Battalion
        fields = ('id', 'action', 'creature_id', 'count_delta', 'level', 'weapon_base_id', 'weapon_material_id')
                    
    def validate(self, data):
        if data['action'] == 'hire':
            try:
                data['creature'] = self.instance.up_opts_creature().get(id=data['creature_id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError("invalid creature_id")
            if not data['count_delta'] or data['count_delta'] < 1 or data['count_delta'] > self.instance.max_hire(data['creature']):
                raise serializers.ValidationError("invalid count_delta")
        if data['action'] == 'fire':
            if not data['count_delta'] or data['count_delta'] < 1 or data['count_delta'] > self.instance.count:
                raise serializers.ValidationError("invalid count_delta")
        if data['action'] == 'train':
            data['cost_xp'] = self.instance.count*self.instance.training_cost_xp_ea()
            if not self.instance.count:
                raise serializers.ValidationError("must have creatures in battalion")
            if data['level'] != self.instance.level+1:
                raise serializers.ValidationError("invalid level")
        if data['action'] == 'arm':
            try:
                data['weapon_base'] = self.instance.up_opts_weapon_base().get(id=data['weapon_base_id'])
                data['weapon_material'] = self.instance.up_opts_weapon_material().get(id=data['weapon_material_id'])
                data['cost_gold'] = self.instance.arm_cost(data['weapon_base'],data['weapon_material'])
                if not self.instance.count:
                    raise serializers.ValidationError("must have creatures in battalion")
                if data['cost_gold'] > self.instance.player.gold:
                    raise serializers.ValidationError("insufficient gold")
            except ObjectDoesNotExist:
                raise serializers.ValidationError("invalid weapon_base_id or weapon_material_id")
        return data        

        
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