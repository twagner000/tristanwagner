from rest_framework import serializers
from .models import Creature, Technology, Structure, Player, LeaderLevel


class BriefCreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature 
        fields = ('id', 'name')


class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature 
        fields = ('pk', 'name', 'plural_name', 'min_ll', 'attack', 'defense', 'cost_cp', 'cost_gold', 'work_gold', 'work_xp', 'oversee')
        #depth = 1


class BriefTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ('id', 'name')
        

class TechnologySerializer(serializers.ModelSerializer):
    prereq = BriefTechnologySerializer(many=True)
    class Meta:
        model = Technology
        fields = ('name', 'level', 'cost', 'prereq')
        
        
class BriefStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ('id', 'name')
        

class StructureSerializer(serializers.ModelSerializer):
    tech_req = BriefTechnologySerializer()
    struct_req = BriefStructureSerializer()
    class Meta:
        model = Structure
        fields = ('name', 'cost_gold', 'cost_xp', 'tech_req', 'struct_req', 'effects')
        
        
class LeaderLevelSerializer(serializers.ModelSerializer):
    enabled_creatures = BriefCreatureSerializer(read_only=True, many=True)
    class Meta:
        model = LeaderLevel
        fields = ('id', 'level', 'life', 'cp', 'xp_cost', 'enabled_creatures')
        

class PlayerSerializer(serializers.ModelSerializer):
    ll = LeaderLevelSerializer()
    technologies = BriefTechnologySerializer(many=True)
    structures = BriefStructureSerializer(many=True)
    class Meta:
        model = Player
        fields = ('id', 'game', 'll', 'technologies', 'structures', 'character_name', 'gold', 'xp', 'calc')
        depth = 1
        

class UpgradeLeaderLevelSerializer(serializers.ModelSerializer):
    current_ll = LeaderLevelSerializer(read_only=True)
    next_ll = LeaderLevelSerializer(read_only=True)
    all_ll = LeaderLevelSerializer(read_only=True, many=True)
    upgrade = serializers.BooleanField()
    
    class Meta:
        model = Player
        fields = ('id', 'current_ll', 'next_ll', 'all_ll', 'xp', 'upgrade')
        read_only_fields = ('xp',)
        
    def validate(self, data):
        next_ll = self.instance.next_ll()
        if not data.get('upgrade',False):
            raise serializers.ValidationError('Did not receive upgrade = True.')
        if not next_ll:
            raise serializers.ValidationError('No upgrade available.')
        if self.instance.xp < next_ll.xp_cost:
            raise serializers.ValidationError('Insufficient xp to upgrade.')
        return data
        
    def update(self, instance, validated_data):
        instance.xp = self.instance.xp - self.instance.next_ll().xp_cost
        instance.ll = self.instance.next_ll()
        instance.save()
        return instance