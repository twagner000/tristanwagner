from rest_framework import serializers
from . import models


class BriefTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ('id', 'full_name')

        
class EntrySerializer(serializers.ModelSerializer):
    task = BriefTaskSerializer()
    
    class Meta:
        model = models.Entry
        fields = ('id', 'owner', 'task', 'start', 'end', 'comments', 'date_updated', 'hours')
        
        
#battalions = BriefBattalionSerializer(many=True)