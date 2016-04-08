from django.contrib import admin
from .models import Puzzle

class PuzzleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Puzzle, PuzzleAdmin)