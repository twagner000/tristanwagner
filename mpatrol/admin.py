from django.contrib import admin
from .models import Game, Player, Battalion, LeaderLevel, Creature, Technology, Structure, WeaponBase, WeaponMaterial

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'started_date', 'ended_date')

    
class BattalionInline(admin.TabularInline):
    model = Battalion

    
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'character_name', 'll', 'gold', 'xp')
    list_filter = ['game']
    inlines = [BattalionInline]


class LeaderLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'life', 'cp', 'xp_cost')


class CreatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'plural_name', 'min_ll', 'attack', 'defense', 'cost_cp', 'cost_gold', 'work_gold', 'work_xp', 'oversee')

    
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'cost', 'prereq_names')
    
    
class StructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_gold', 'cost_xp', 'tech_req', 'struct_req', 'effects')
    
    
class WeaponBaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'tech_req', 'struct_req', 'attack_mult', 'cost_gold')
    
    
class WeaponMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'tech_req', 'struct_req', 'attack_mult', 'cost_mult', 'armor')
    
    
admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(LeaderLevel, LeaderLevelAdmin)
admin.site.register(Creature, CreatureAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Structure, StructureAdmin)
admin.site.register(WeaponBase, WeaponBaseAdmin)
admin.site.register(WeaponMaterial, WeaponMaterialAdmin)


