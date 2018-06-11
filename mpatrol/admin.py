from django.contrib import admin
from .models import Creature

class CreatureAdmin(admin.ModelAdmin):
    list_display = ('name','min_ll','attack','defense','cost_cp','cost_gold','work_gold','work_exp','oversee')

admin.site.register(Creature, CreatureAdmin)
