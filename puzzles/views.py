from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.utils import timezone
from .models import Puzzle

def index(request):
    latest_released_puzzle_list = Puzzle.objects.filter(release_date__lte=timezone.now()).order_by('-release_date')[:3]
    return render(request, 'puzzles/index.html', {'latest_released_puzzle_list':latest_released_puzzle_list})
        
class PuzzleDetail(DetailView):
    context_object_name = 'puzzle'
    queryset = Puzzle.objects.filter(release_date__lte=timezone.now())