from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import serializers
import json
from . import models


class JSONTextField(serializers.Field):
    def to_internal_value(self, obj):
        return json.dumps(obj)

    def to_representation(self, data):
        return json.loads(data) if data else None
        
        
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
            if not self.instance.count:
                raise serializers.ValidationError("must have creatures in battalion")
            data['cost_xp'] = self.instance.count*self.instance.training_cost_xp_ea()
            if data['cost_xp'] > self.instance.player.xp:
                raise serializers.ValidationError("insufficient xp")
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
        fields = ('id', 'name', 'started_date')
        
        
class GamePlayerSerializer(BriefGameSerializer):
    player = serializers.SerializerMethodField()
    
    class Meta(BriefGameSerializer.Meta):
        fields = BriefGameSerializer.Meta.fields + ('player',)
        
    def get_player(self,obj):
        try:
            player = obj.player_set.get(user=self.context['request'].user)
            serializer = PublicPlayerSerializer(player, read_only=True)
            return serializer.data
        except ObjectDoesNotExist:
            return None
        
        
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
        

class PlayerActionSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(models.PlayerLog.ACTIONS, write_only=True)
    target_player_id = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    
    class Meta:
        model = models.Player
        fields = ('id', 'action', 'target_player_id')
    
    def validate(self, data):
        if data['target_player_id'] == self.instance.id:
            raise serializers.ValidationError("Cannot target self for action.")
        if not self.instance.avail_action_points():
            raise serializers.ValidationError("No action points available.")
        if data['action'] == 'spy' or data['action'] == 'attack':
            try:
                data['target_player'] = self.instance.game.player_set.get(id=data['target_player_id'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Invalid target player.")
            if data['target_player'].is_protected():
                raise serializers.ValidationError("Target player is protected by the Guardians.")
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
        fields = ('id', 'game', 'character_name', 'll', 'gold', 'xp', 'avail_action_points', 'static_score', 'score_rank',
                  'technologies', 'structures', 'battalions', 'calc',
                  'up_opt_ll', 'up_opts_structure', 'up_opts_technology')
                  

class PublicPlayerSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=models.Game.objects.all())
    class Meta:
        model = models.Player
        fields = ('game', 'id', 'character_name', 'is_protected')
        read_only_fields = ('id', 'is_protected',)


class ChoosePlayerSerializer(PublicPlayerSerializer):
    game__name = serializers.SerializerMethodField()
    game__started_date = serializers.SerializerMethodField()
    
    class Meta(PublicPlayerSerializer.Meta):
        fields = PublicPlayerSerializer.Meta.fields + ('game__name', 'game__started_date')
        
    def get_game__name(self,obj):
        return obj.game.name
        
    def get_game__started_date(self,obj):
        return obj.game.started_date

        
class PlayerScoreSerializer(PublicPlayerSerializer):
    class Meta(PublicPlayerSerializer.Meta):
        fields = PublicPlayerSerializer.Meta.fields + ('score_rank', 'static_score')
        
        
class PlayerLogSerializer(serializers.ModelSerializer):
    json_data = JSONTextField()
    target_player = PublicPlayerSerializer()
    
    class Meta:
        model = models.PlayerLog
        fields = ('player', 'target_player', 'date', 'action', 'action_points', 'description', 'json_data', 'success')

