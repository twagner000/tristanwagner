from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(get_user_model(), models.PROTECT, related_name='projects_owned')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    
    #use 'team' for top-level projects only
    team = models.ManyToManyField(get_user_model(), blank=True, related_name='projects_on')
    
    class Meta:
        ordering = ['-date_created']
        unique_together = (('parent', 'name',),)
    
    def is_active(self):
        return not self.date_closed
        
    def get_team(self):
        if self.parent:
            return self.parent.get_team()
        return self.team
        
    def __str__(self):
        if self.parent:
            return '{} > {}'.format(self.parent,self.name)
        return self.name
        
    
class Task(models.Model):
    project = models.ForeignKey(Project, models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(get_user_model(), models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    est_hours = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
        unique_together = (('project', 'name',),)
    
    def is_active(self):
        return not self.date_closed
        
    def full_name(self):
        return str(self)
        
    def __str__(self):
        return '{} > {}'.format(self.project,self.name)
        
        
    
class Entry(models.Model):
    owner = models.ForeignKey(get_user_model(), models.PROTECT)
    task = models.ForeignKey(Task, models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    #hours (store calculated value on save? would this work better with aggregation functions?)
    
    class Meta:
        ordering = ['-start']
        
    def hours(self):
        if not self.end:
            return None
        return (self.end - self.start).total_seconds()/3600
        
    def task_obj(self):
        return self.task
        
    def __str__(self):
        return '{} hrs on {} by {}'.format(self.hours(), self.start.strftime('%Y-%m-%d'), str(self.owner))
        #{:.2f}
        