from django.db import models
from django.contrib.auth import get_user_model


class Project(models.Model):
    parent = models.ForeignKey('self', models.CASCADE, null=True, blank=True, related_name='project_set')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(get_user_model(), models.PROTECT, related_name='projects_owned')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_closed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_created']
        unique_together = (('parent', 'name',),)
        
    def top_level_project(self):
        top_level_project = self
        while top_level_project.parent:
            top_level_project = top_level_project.parent
        return top_level_project
    
    def is_active(self):
        return not self.date_closed
        
    def project_list(self):
        if self.parent:
            proj_list = self.parent.project_list()[:]
            proj_list.append({'id':self.id,'name':self.name})
            return proj_list
        else:
            return [{'id':self.id,'name':self.name}]
        
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
        
    def project_list(self):
        return self.project.project_list()
        
    def __str__(self):
        return '{} > {}'.format(self.project,self.name)
        
        
    
class Entry(models.Model):
    owner = models.ForeignKey(get_user_model(), models.PROTECT)
    task = models.ForeignKey(Task, models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    hours = models.FloatField(editable=False, default=0)
    
    class Meta:
        ordering = ['-start']
        
    def save(self, *args, **kwargs):
        self.hours = 0 if not self.end else (self.end - self.start).total_seconds()/3600
        super(Entry, self).save(*args, **kwargs)
        
    def __str__(self):
        return '{:.2f} hrs on {} by {}'.format(self.hours, self.start.strftime('%Y-%m-%d'), str(self.owner))
        