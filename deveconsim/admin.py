from django.contrib import admin
from .models import Game, Turn

class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'started_date', 'completed_date')
    list_filter = ['user']

class TurnAdmin(admin.ModelAdmin):
    list_display = ('game', 'turn', 'started_date', 'completed_date')
    list_filter = ['game']

admin.site.register(Game, GameAdmin)
admin.site.register(Turn, TurnAdmin)
