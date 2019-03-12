from rest_framework import serializers
from . import models

class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BGGPlay
        fields = ('date', 'timestamp', 'game_name', 'quantity')
        
class PlayDateSerializer(serializers.ModelSerializer):
    plays = PlaySerializer(many=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = models.BGGPlayDate
        fields = ('date','plays','total',)
        
    def get_total(self, obj):
        return obj.plays().count()
    




