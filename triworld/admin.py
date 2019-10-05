from django.contrib import admin

from . import models


class WorldAdmin(admin.ModelAdmin):
    list_display = ('date_created',)
    
class MajorTriAdmin(admin.ModelAdmin):
    list_display = ('face','major_row','major_col','sea')
    list_filter = ('face',)


admin.site.register(models.World, WorldAdmin)
admin.site.register(models.Face)
admin.site.register(models.MajorTri, MajorTriAdmin)
admin.site.register(models.MinorTri)
