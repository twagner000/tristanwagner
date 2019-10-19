#from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import serializers
import json

from . import models


class BriefWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.World
        fields = ('id', 'major_dim', 'minor_dim', 'date_created')
        
    def validate_major_dim(self,value):
        if not value%3==0 or value <= 0:
            raise serializers.ValidationError("Major dimension must be a postive multiple of 3.")
        return value
        
    def validate_minor_dim(self,value):
        if value < 3:
            raise serializers.ValidationError("Minor dimension must be at least 3.")
        return value
        
        
class BriefMajorTriSerializer(serializers.ModelSerializer):
    cached_neighbor_ids = serializers.SerializerMethodField()
    
    class Meta:
        model = models.MajorTri
        #fields reserved for js use: rn, tpd
        fields = ('id', 'i', 'ri', 'ci', 'sea', 'ice', 'cached_neighbor_ids',)
        
    def get_cached_neighbor_ids(self,obj):
        return json.loads(obj.cached_neighbor_ids)
        

class FaceSerializer(serializers.ModelSerializer):
    #majortri_set = BriefMajorTriSerializer(many=True)
    
    class Meta:
        model = models.Face
        fields = ('id', 'ring', 'ring_i', 'fpd', 'neighbor_ids', 'majortri_set')


class WorldSerializer(BriefWorldSerializer):
    faces = serializers.SerializerMethodField()
    majortris = serializers.SerializerMethodField()
    
    class Meta(BriefWorldSerializer.Meta):
        fields = BriefWorldSerializer.Meta.fields + ('home_face_id', 'faces', 'majortris')
        
    def get_faces(self,obj):
        faces = FaceSerializer(obj.face_set.all(), many=True)
        return dict((f['id'],f) for f in faces.data)
        
    def get_majortris(self,obj):
        majortris = BriefMajorTriSerializer(models.MajorTri.objects.filter(face__world=obj), many=True)
        return dict((t['id'],t) for t in majortris.data)
        
        
class MinorTriSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MinorTri
        fields = ('id', 'i', 'ri', 'ci',)
        
                
        
class MajorTriSerializer(BriefMajorTriSerializer):
    minortri_set = MinorTriSerializer(many=True)
    
    class Meta(BriefMajorTriSerializer.Meta):
        #note: angles in neighbor_ids will NOT match for polar sides!!!)
        fields = BriefMajorTriSerializer.Meta.fields + ('minortri_set',)
        
