from django.contrib import admin
from . import models

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'started_date', 'ended_date')

    
class BattalionInline(admin.TabularInline):
    model = models.Battalion

    
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'character_name', 'll', 'static_score', 'gold', 'xp')
    list_filter = ['game']
    inlines = [BattalionInline]


class LeaderLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'life', 'cp', 'cost_xp')


class CreatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'plural_name', 'min_ll', 'attack', 'defense', 'cost_cp', 'cost_gold', 'work_gold', 'work_xp', 'oversee')

    
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_ll', 'cost_xp', 'prereq_names')
    
    
class StructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_gold', 'cost_xp', 'tech_req', 'struct_req', 'effects')
    
    
class WeaponBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'tech_req', 'struct_req', 'attack_mult', 'cost_gold')
    
    
class WeaponMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'tech_req', 'struct_req', 'attack_mult', 'cost_mult', 'armor')
    
    
class PlayerLogAdmin(admin.ModelAdmin):
    list_display = ('player','date','action','action_points','description')
    
    
admin.site.register(models.Game, GameAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.LeaderLevel, LeaderLevelAdmin)
admin.site.register(models.Creature, CreatureAdmin)
admin.site.register(models.Technology, TechnologyAdmin)
admin.site.register(models.Structure, StructureAdmin)
admin.site.register(models.WeaponBase, WeaponBaseAdmin)
admin.site.register(models.WeaponMaterial, WeaponMaterialAdmin)
admin.site.register(models.PlayerLog, PlayerLogAdmin)

