from django.contrib import admin
from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'owner', 'date_created', 'date_closed')
    list_filter = ['parent', 'owner']
    
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'owner', 'date_created', 'date_closed', 'est_hours')
    list_filter = ['project', 'owner']

    
class EntryAdmin(admin.ModelAdmin):
    list_display = ('task', 'owner', 'start', 'end', 'hours')
    list_filter = ['task', 'owner']
    

admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Entry, EntryAdmin)