from django.shortcuts import render, redirect

def index(request):
    return render(request, 'puzzles/index.html', {})
    
def solved(request):
    if request.POST.get('solution', '').lower() == 'scotch':
        return render(request, 'puzzles/solved.html', {})
    else:
        return redirect('puzzles:wrong')
        
def wrong(request):
    return render(request, 'puzzles/wrong.html')