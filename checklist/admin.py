from django.contrib import admin
from .models import Checklist, QuestionGroup, Question, AnsweredChecklist, AnsweredQuestion

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class QuestionGroupAdmin(admin.ModelAdmin):
    model = QuestionGroup
    extra = 3
    inlines = [QuestionInline]
    list_display = ('__unicode__', 'checklist', 'sequence')
    list_filter = ['checklist']

class ChecklistAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'owner')
    list_filter = ['owner']

class AnsweredQuestionInline(admin.StackedInline):
    model = AnsweredQuestion

class AnsweredChecklistAdmin(admin.ModelAdmin):
    inlines = [AnsweredQuestionInline]
    list_display = ('checklist', 'for_date', 'created_date', 'ans_by')
    list_filter = ['checklist', 'for_date', 'created_date', 'ans_by']

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(AnsweredChecklist, AnsweredChecklistAdmin)
