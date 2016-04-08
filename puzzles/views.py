from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Puzzle

def index(request):
    latest_released_puzzle_list = Puzzle.objects.filter(release_date__lte=timezone.now()).order_by('-release_date')[:3]
    return render(request, 'puzzles/index.html', {'latest_released_puzzle_list':latest_released_puzzle_list})
            
def check(request, slug):
    puzzle = get_object_or_404(Puzzle, slug=slug)
    if request.POST.get('solution', '').lower() == puzzle.solution.lower():
        return render(request, 'puzzles/success.html', {'puzzle':puzzle})
    else:
        return render(request, 'puzzles/fail.html', {'puzzle':puzzle})
    
def puzzle_detail(request, slug):
    puzzle = get_object_or_404(Puzzle, slug=slug)
    return render(request, 'puzzles/detail.html', {'puzzle':puzzle})