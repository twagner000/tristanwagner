from django.contrib import admin

from . import models

class BoardGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'objectid', 'date_updated')

class GameFactorsAdmin(admin.ModelAdmin):
    list_display = ('game', 'bias', 'date_updated')
    
class GameNeighborAdmin(admin.ModelAdmin):
    list_display = ('game', 'neighbor', 'rank', 'distance', 'date_updated')
    

admin.site.register(models.BoardGame, BoardGameAdmin)
admin.site.register(models.GameFactors, GameFactorsAdmin)
admin.site.register(models.GameNeighbor, GameNeighborAdmin)
