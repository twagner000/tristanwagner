from django.db import models

from . import constants

class Creature(models.Model):
    name = models.CharField(unique=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    min_ll = models.PositiveIntegerField(default=1, verbose_name='Min Leader Level')
    attack = models.PositiveIntegerField(default=0)
    defense = models.PositiveIntegerField(default=0)
    cost_cp = models.PositiveIntegerField(default=1, verbose_name='Cost in Creature Points')
    cost_gold = models.PositiveIntegerField(default=20, verbose_name='Cost in Gold')
    work_gold = models.PositiveIntegerField(default=5, verbose_name='Gold from Working')
    work_exp = models.PositiveIntegerField(default=1, verbose_name='Experience from Working')
    oversee = models.PositiveIntegerField(default=0, verbose_name='Overseeing Capability')
    
    class Meta:
        ordering = ['min_ll','cost_cp','cost_gold','work_gold','work_exp']
    
    def __str__(self):
        return self.name
