#from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import serializers
#import json

from . import models


class WorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.World
        fields = ('id', 'major_dim', 'minor_dim', 'date_created')


class BriefFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Face
        fields = ('id', 'face_ring', 'face_index')        
        
        
class MajorTriSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MajorTri
        fields = ('id', 'major_row', 'major_col', 'sea')


class FaceSerializer(BriefFaceSerializer):
    map = serializers.SerializerMethodField()
    
    class Meta(BriefFaceSerializer.Meta):
        fields = BriefFaceSerializer.Meta.fields + ('points_down', 'map', )
        
    def get_map(self,obj):
        n = obj.world.major_dim
        adj_faces = obj.adj_faces()
        all_tri = obj.majortri_set
        rows = [all_tri.filter(major_row=(ri-2 if obj.points_down() else n-1-ri)) for ri in range(n*4//3)]
        serialized_rows = [MajorTriSerializer(x, many=True).data for x in rows]
        return {'adj_faces': BriefFaceSerializer(obj.adj_faces(), many=True).data, 'rows': serialized_rows}



"""class GamePlayerSerializer(BriefGameSerializer):
    player = serializers.SerializerMethodField()
    
    class Meta(BriefGameSerializer.Meta):
        fields = BriefGameSerializer.Meta.fields + ('player',)
        
    def get_player(self,obj):
        try:
            player = obj.player_set.get(user=self.context['request'].user)
            serializer = PublicPlayerSerializer(player, read_only=True)
            return serializer.data
        except ObjectDoesNotExist:
            return None"""