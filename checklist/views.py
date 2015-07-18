from django.shortcuts import render, get_object_or_404, redirect
from .models import Checklist, AnsweredChecklist

def index(request):
    checklist_list = Checklist.objects.all()
    return render(request, 'checklist/index.html', {'checklist_list': checklist_list})

def take(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    return render(request, 'checklist/take.html', {'checklist': checklist})

def history(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if request.user.is_authenticated():
        ans_checklist_list = AnsweredChecklist.objects.filter(ans_by=request.user).filter(checklist=checklist).order_by('-for_date')
        return render(request, 'checklist/history.html', {'checklist': checklist, 'ans_checklist_list': ans_checklist_list})        
    return render(request, 'checklist/history.html', {'checklist': checklist})

def results(request, ans_checklist_id):
    if request.user.is_authenticated():
        ans_checklist_list = AnsweredChecklist.objects.filter(ans_by=request.user)
        ans_checklist = get_object_or_404(ans_checklist_list, pk=ans_checklist_id)
        return render(request, 'checklist/results.html', {'ans_checklist': ans_checklist})
    return render(request, 'checklist/results.html')

def submit(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    if not request.user.is_authenticated():
        return render(request, 'checklist/take.html', {
            'checklist': checklist,
            'error_message': "You must be logged in to submit a completed checklist.",
        })
    ac = AnsweredChecklist(checklist=checklist, ans_by=request.user)
    ac.save()
    for gr in checklist.questiongroup_set.all():
        for qu in gr.question_set.all():
            ac.answeredquestion_set.create(question=qu, score=request.POST.get('q%d' % qu.id, default=0), comment=request.POST.get('qc%d' % qu.id, default=None))
    ac.save()
    return redirect('checklist:results', ans_checklist_id=ac.id)
