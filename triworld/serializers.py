#from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import serializers
import json

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
    points_down = serializers.SerializerMethodField()
    map = serializers.SerializerMethodField()
    neighbor_ids = serializers.SerializerMethodField()
    
    class Meta(BriefFaceSerializer.Meta):
        fields = BriefFaceSerializer.Meta.fields + ('points_down', 'neighbor_ids', 'map')
        
    def get_points_down(self,obj):
        return obj.faceext.points_down
        
    def get_neighbor_ids(self,obj):
        return json.loads(obj.faceext.neighbor_ids)
        
    def get_map(self,obj):
        f = obj.faceext.refresh()
        f.save()
        return json.loads(obj.faceext.map)



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