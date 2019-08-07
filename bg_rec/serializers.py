from rest_framework import serializers
from . import models

class BriefBoardGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoardGame
        fields = ('objectid', 'name')

class BoardGameSerializer(BriefBoardGameSerializer):
    class Meta(BriefBoardGameSerializer.Meta):
        fields = BriefBoardGameSerializer.Meta.fields + ('yearpublished', 'minplayers', 'maxplayers', 'minplaytime', 'maxplaytime', 'playingtime', 'average', 'bayesaverage', 'usersrated', 'averageweight', 'thumbnail',)

class NeighborSerializer(serializers.ModelSerializer):
    neighbor = BoardGameSerializer()
    
    class Meta:
        model = models.GameNeighbor
        fields = ('game', 'neighbor', 'distance')

class BoardGameSearchSerializer(BoardGameSerializer):
    gameneighbor_set = NeighborSerializer(many=True)
    
    class Meta(BoardGameSerializer.Meta):
        fields = BoardGameSerializer.Meta.fields + ('gameneighbor_set',)
