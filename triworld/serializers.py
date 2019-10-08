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


class FaceSerializer(BriefFaceSerializer):
    world_id = serializers.SerializerMethodField()
    major_dim = serializers.SerializerMethodField()
    map = serializers.SerializerMethodField()
    
    class Meta(BriefFaceSerializer.Meta):
        fields = BriefFaceSerializer.Meta.fields + ('world_id', 'points_down', 'major_dim', 'neighbor_ids', 'map')
        
    def get_world_id(self,obj):
        return obj.world.id
        
    def get_major_dim(self,obj):
        return obj.world.major_dim
        
    def get_map(self,obj):
        map = obj.map()
        #do this in serializer so that can use MajorTriSerializer to generate stored JSON
        if not map:
            map = obj.generate_map()
            map = [MajorTriSerializer(row, many=True).data for row in map]
            obj._map = json.dumps(map)
            obj.save()
        return map


class MajorTriSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MajorTri
        fields = ('id', 'face', 'major_row', 'major_col', 'sea', 'get_r2_left', 'get_r2_right')


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