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
        fields = ('id', 'name', 'level', 'cost_xp', 'prereq')
        
        
class BriefStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = ('id', 'name')
        

class StructureSerializer(serializers.ModelSerializer):
    tech_req = BriefTechnologySerializer()
    struct_req = BriefStructureSerializer()
    class Meta:
        model = Structure
        fields = ('id', 'name', 'cost_gold', 'cost_xp', 'tech_req', 'struct_req', 'effects')
        
        
class BriefLeaderLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderLevel
        fields = ('id', 'level')
        
        
class LeaderLevelSerializer(serializers.ModelSerializer):
    enabled_creatures = BriefCreatureSerializer(read_only=True, many=True)
    class Meta:
        model = LeaderLevel
        fields = ('id', 'level', 'life', 'cp', 'xp_cost', 'enabled_creatures')
        

class PlayerSerializer(serializers.ModelSerializer):
    ll = LeaderLevelSerializer()
    technologies = BriefTechnologySerializer(many=True)
    structures = BriefStructureSerializer(many=True)
    ll_upgrade = LeaderLevelSerializer()
    structure_upgrade = StructureSerializer(many=True)
    technology_upgrade = TechnologySerializer(many=True)
    
    class Meta:
        model = Player
        fields = ('id', 'game', 'character_name', 'll', 'gold', 'xp', 'technologies', 'structures', 'calc', 'll_upgrade', 'structure_upgrade', 'technology_upgrade')