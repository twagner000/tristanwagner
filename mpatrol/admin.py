from django.contrib import admin
from .models import Game, Player, Battalion

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'started_date', 'ended_date')

    
class BattalionInline(admin.TabularInline):
    model = Battalion
    
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'll', 'gold', 'xp')
    list_filter = ['game']
    inlines = [BattalionInline]

admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)

