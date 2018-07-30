from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.utils import timezone
from django.conf import settings

from . import models

def index(request):
    latest_released_puzzle_list = models.Puzzle.objects.filter(release_date__lte=timezone.now()).order_by('-release_date')[:3]
    return render(request, 'puzzles/index.html', {'latest_released_puzzle_list':latest_released_puzzle_list, 'project_euler_user': settings.PROJECT_EULER_USER})
        
class PuzzleDetail(DetailView):
    context_object_name = 'puzzle'
    queryset = models.Puzzle.objects.filter(release_date__lte=timezone.now())