from rest_framework import serializers
from . import models


class BriefTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ('id', 'full_name')

        
class EntrySerializer(serializers.ModelSerializer):
    task_obj = BriefTaskSerializer(read_only=True)
    
    class Meta:
        model = models.Entry
        fields = ('id', 'owner', 'task', 'start', 'end', 'comments', 'task_obj', 'date_updated', 'hours')
        read_only_fields = ('owner',)
        
#battalions = BriefBattalionSerializer(many=True)