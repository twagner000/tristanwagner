from rest_framework import serializers
from .models import Creature, Technology, Player

class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature 
        fields = ('pk', 'name', 'plural_name', 'min_ll', 'attack', 'defense', 'cost_cp', 'cost_gold', 'work_gold', 'work_xp', 'oversee')
        #depth = 1


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology 
        fields = ('name', 'level', 'cost', 'prereq', 'prereq_names')
        #depth = 1
        

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player 
        fields = ('id', 'game', 'll', 'technologies', 'structures', 'character_name', 'gold', 'xp', 'calc')
        depth = 1