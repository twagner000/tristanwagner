from rest_framework import serializers
from .models import Creature, Technology

class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature 
        fields = ('name', 'plural_name', 'min_ll', 'attack', 'defense', 'cost_cp', 'cost_gold', 'work_gold', 'work_xp', 'oversee')
        #depth = 1


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology 
        fields = ('name', 'level', 'cost', 'prereq', 'prereq_names')
        #depth = 1