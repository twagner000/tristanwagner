from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Case, When, IntegerField, FloatField

from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

import itertools
import datetime
import collections

from . import models
from . import serializers

AUTH_OFF = True

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user        


class IndexView(TemplateView):
    template_name = 'timetracker/index.html'
    
    
class EntryViewSet(viewsets.ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    permission_classes = [permissions.AllowAny] if AUTH_OFF else [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        q = super().get_queryset()
        return q if AUTH_OFF else q.filter(owner=self.request.user)
        
    @action(detail=False)
    def recent(self, request):
        q = self.get_queryset()
        q = itertools.chain(q.filter(end=None),q.exclude(end=None)[:3])
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)
        
    @action(detail=False)
    def open(self, request):
        q = self.get_queryset().filter(end=None)
        serializer = self.get_serializer(q, many=True)
        return Response(serializer.data)
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    '''def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [permissions.IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]'''
        
class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.BriefTaskSerializer
    permission_classes = [permissions.AllowAny] if AUTH_OFF else [permissions.IsAuthenticated, IsOwner]
   

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.BriefProjectSerializer
    permission_classes = [permissions.AllowAny] if AUTH_OFF else [permissions.IsAuthenticated, IsOwner]
        
'''class DateRangeProjectList(generics.ListAPIView):
    serializer_class = serializers.BriefTaskSerializerWithEntryCount
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        (start,end) = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in self.kwargs['period'].split('-to-')]
        print(start)
        print(end)
        #q = models.Task.objects.annotate(entry_count=Count('entry')).filter(entry_count__gt=0)
        q = models.Task.objects.annotate(
            entry_count=Count(Case(
                When(entry__start__gte=start, entry__end__lte=end, then=1),
                output_field=IntegerField(),
            ))
        ).filter(entry_count__gt=0)
        return q'''
        
class DateRangeProjectList(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        (start,end) = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in kwargs['period'].split('-to-')]
        '''entries = models.Entry.objects.filter(start__gte=start, end__lte=end)
        tasks = models.Task.objects.filter(id__in=entries.values_list('task', flat=True))
        proj_ids = [t.project_list() for t in tasks]
        proj_ids = [t[0]['id'] for t in proj_ids if len(t)>0]
        projects = models.Project.objects.filter(id__in=proj_ids)
        entries = serializers.BriefEntrySerializer(entries, many=True).data
        tasks = serializers.BriefTaskSerializerWithProjectList(tasks, many=True).data
        projects = serializers.BriefProjectSerializer(projects, many=True).data
        for t in tasks:
            t['entries'] = []
        for e in entries:
            for t in tasks:
                if e['task'] == t['id']:
                    t['entries'].append(e)
                    break
        return Response({'projects': projects, 'tasks': tasks, 'entries': entries})'''
        
        entries = models.Entry.objects.filter(start__gte=start, end__lte=end)
        ser_entries = serializers.FlatEntrySerializer(entries, many=True).data
        
        task_hrs = collections.defaultdict(float)
        tlproj_hrs = collections.defaultdict(float)
        for e in entries:
            task_hrs[e.task.id] += e.hours
            tlproj_hrs[e.task.project.top_level_project().id] += e.hours
        
        tasks = models.Task.objects.filter(id__in=task_hrs.keys())
        ser_tasks = serializers.BriefTaskSerializerWithHours(tasks, many=True).data
        projects = models.Project.objects.filter(id__in=tlproj_hrs)
        ser_projects = serializers.BriefProjectSerializer(projects, many=True).data
        
        for t in ser_tasks:
            t['hours'] = task_hrs.get(t['id'],0)
            t['entries'] = []
            for e in ser_entries:
                if e['task'] == t['id']:
                    t['entries'].append(e)
        for p in ser_projects:
            p['hours'] = tlproj_hrs.get(p['id'],0)
            p['tasks'] = []
            for t in ser_tasks:
                if t['top_level_project'] == p['id']:
                    p['tasks'].append(t)
        
        return Response({'start': start, 'end': end, 'results': ser_projects})
        
        
        #serializer = serializers.EntrySerializer(entries, many=True)
        #return Response(serializer.data)
    
   
'''class PlayDateList(generics.ListAPIView):
    queryset = models.BGGPlayDate.objects.filter(date__gte=datetime.date(datetime.date.today().year,1,1), date__lte=datetime.date.today())
    serializer_class = serializers.PlayDateSerializer
    permission_classes = tuple()
    
class PlayList(generics.ListAPIView):
    queryset = models.BGGPlay.objects.filter(date__gte=datetime.date(datetime.date.today().year,1,1), date__lte=datetime.date.today())
    serializer_class = serializers.PlaySerializer
    permission_classes = tuple()
    
class Past52WeeksList(APIView):
    permission_classes = tuple()

    def get(self, request, format=None):
        weeks = []
        cur_week_start = datetime.date.today()
        cur_week_start -= datetime.timedelta(days=cur_week_start.weekday())
        cur_week_start -= datetime.timedelta(days=52*7)
        for i in range(52):
            next_week_start = cur_week_start + datetime.timedelta(days=7)
            weeks.append({'week':cur_week_start, 'count':models.BGGPlay.objects.filter(date__gte=cur_week_start, date__lt=next_week_start).count()})
            cur_week_start = next_week_start
        return Response(weeks)'''
    
