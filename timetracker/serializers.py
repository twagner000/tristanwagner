from rest_framework import serializers
from . import models


class BriefTaskSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Task
        fields = ('id', 'full_name')
        
    def get_full_name(self, obj):
        return str(obj)
        

        
        
class BriefTaskSerializerWithHours(BriefTaskSerializer):
    hours = serializers.FloatField(default=0)
    top_level_project = serializers.SerializerMethodField()
    
    class Meta(BriefTaskSerializer.Meta):
        fields = BriefTaskSerializer.Meta.fields + ('hours', 'top_level_project')
        
    def get_top_level_project(self, obj):
        return obj.project.top_level_project().id
        
        
        
        
        
class BriefProjectSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Project
        fields = ('id', 'name', 'full_name', 'parent')
        read_only_fields = ('owner', 'parent_obj')
        
    def get_full_name(self, obj):
        return str(obj)

        

        
class ProjectSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    parent_obj = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Project
        fields = ('id', 'name', 'parent', 'description', 'owner', 'date_created', 'date_closed', 'full_name', 'parent_obj', 'date_updated')
        read_only_fields = ('owner',)
        
    def get_full_name(self, obj):
        return str(obj)
        
    def get_parent_obj(self, obj):
        if obj.parent:
            return BriefProjectSerializer(obj.parent).data
        return None
        
        
class BriefTaskSerializerWithProject(BriefTaskSerializer):
    project_obj = serializers.SerializerMethodField()
    
    class Meta(BriefTaskSerializer.Meta):
        fields = BriefTaskSerializer.Meta.fields + ('project', 'name', 'project_obj')
        
    def get_project_obj(self, obj):
        return ProjectSerializer(obj.project).data
        
class BriefEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = ('id', 'task', 'start', 'end', 'hours', 'comments')
        read_only_fields = tuple()

class EntrySerializer(BriefEntrySerializer):
    task_obj = serializers.SerializerMethodField()
    
    class Meta(BriefEntrySerializer.Meta):
        fields = BriefEntrySerializer.Meta.fields + ('owner', 'task_obj', 'date_updated')
        read_only_fields = BriefEntrySerializer.Meta.read_only_fields + ('owner',)
        
    def get_task_obj(self, obj):
        return BriefTaskSerializerWithProject(obj.task).data
        
        
class FlatEntrySerializer(BriefEntrySerializer):
    task__name = serializers.SerializerMethodField()
    task__full_name = serializers.SerializerMethodField()
    task__project = serializers.SerializerMethodField()
    task__project__name = serializers.SerializerMethodField()
    task__project__full_name = serializers.SerializerMethodField()
    task__project__top_level_project = serializers.SerializerMethodField()
    task__project__top_level_project__name = serializers.SerializerMethodField()
    
    class Meta(BriefEntrySerializer.Meta):
        fields = BriefEntrySerializer.Meta.fields + ('task__name', 'task__full_name', 'task__project',
            'task__project__name', 'task__project__full_name', 'task__project__top_level_project', 'task__project__top_level_project__name')
            
    def get_task__name(self, obj):
        return obj.task.name
    
    def get_task__full_name(self, obj):
        return str(obj.task)
    
    def get_task__project(self, obj):
        return obj.task.project.id
    
    def get_task__project__name(self, obj):
        return obj.task.project.name
    
    def get_task__project__full_name(self, obj):
        return str(obj.task.project)
    
    def get_task__project__top_level_project(self, obj):
        return obj.task.project.top_level_project().id
    
    def get_task__project__top_level_project__name(self, obj):
        return obj.task.project.top_level_project().name
    
    
    
    
    