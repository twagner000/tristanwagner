from django.contrib import admin

from . import models


class WorldAdmin(admin.ModelAdmin):
    list_display = ('date_created',)
    
class FaceAdmin(admin.ModelAdmin):
    list_filter = ('world',)
    
class MajorTriAdmin(admin.ModelAdmin):
    list_display = ('face','i','sea','ice')
    list_filter = ('face',)
    
class MinorTriAdmin(admin.ModelAdmin):
    list_display = ('major_tri','i','ri','ci')
    list_filter = ('major_tri',)


admin.site.register(models.World, WorldAdmin)
admin.site.register(models.Face, FaceAdmin)
admin.site.register(models.MajorTri, MajorTriAdmin)
admin.site.register(models.MinorTri, MinorTriAdmin)
