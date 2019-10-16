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
        
        
class MajorTriSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MajorTri
        #fields reserved for js use: ri, ci, rn, tpd
        #note: angles in neighbor_ids will NOT match for polar sides!!!
        fields = ('id', 'i', 'rci', 'sea', 'ice',) #'neighbor_ids')
        

class FaceSerializer(serializers.ModelSerializer):
    majortris = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Face
        fields = ('id', 'ring', 'ring_i', 'fpd', 'neighbor_ids', 'majortris')
        
    def get_majortris(self,obj):
        #return obj.majortris()
        return MajorTriSerializer(obj.majortri_set.all(), many=True).data


class WorldSerializer(BriefWorldSerializer):
    faces = serializers.SerializerMethodField()
    
    class Meta(BriefWorldSerializer.Meta):
        fields = BriefWorldSerializer.Meta.fields + ('home_face_id', 'faces')
        
    def get_faces(self,obj):
        faces = FaceSerializer(obj.face_set.all(), many=True)
        return dict((f['id'],f) for f in faces.data)
        
