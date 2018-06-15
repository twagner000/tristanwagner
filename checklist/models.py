from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone

class Checklist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name

class QuestionGroup(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sequence = models.PositiveIntegerField(default=10)
    help = models.TextField(blank=True)
    
    class Meta:
        ordering = ['checklist','sequence']

    def __str__(self):
        return "%s: %s" % (self.checklist,self.name)
        
class Question(models.Model):
    question_group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    sequence = models.PositiveIntegerField(default=10)
    weight = models.PositiveIntegerField(default=10)
    help = models.TextField(blank=True)
    
    class Meta:
        ordering = ['question_group','sequence']

    def __str__(self):
        return self.question

class AnsweredChecklist(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    for_date = models.DateField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    ans_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.checklist, self.ans_by)

    def score(self):
        actual = self.answeredquestion_set.aggregate(Sum('score'))['score__sum']
        maxposs = self.answeredquestion_set.count()*5
        pct = 1000*actual/maxposs
        pct /= 10.0
        groups = QuestionGroup.objects.filter(checklist=self.checklist).order_by('sequence')
        groups = [{'name':gr.name, 'pk':gr.pk, 'ansqu':self.answeredquestion_set.filter(question__question_group__pk=gr.pk)} for gr in groups]
        for gr in groups:
            gr['score'] = gr['ansqu'].aggregate(Sum('score'))['score__sum']
            gr['maxposs'] = len(gr['ansqu'])*5
        return {'actual':actual, 'max':maxposs, 'pct':pct, 'groups':groups}

class AnsweredQuestion(models.Model):
    ans_checklist = models.ForeignKey(AnsweredChecklist, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return "%s (%d)" % (self.question, self.score)

    def has_comment(self):
        return True if self.comment else False