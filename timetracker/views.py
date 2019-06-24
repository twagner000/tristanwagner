from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import models
#from rest_framework import generics

#@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'timetracker/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_entries = models.Entry.objects.filter(user=self.request.user)
            context['open_entries'] = user_entries.filter(end=None)
            context['recent_entries'] = user_entries.exclude(end=None)[:3]
        return context
    
    
'''class PlayList(generics.ListAPIView):
    queryset = models.BGGPlay.objects.filter(date__gte=datetime.date(datetime.date.today().year,1,1), date__lte=datetime.date.today())
    serializer_class = serializers.PlaySerializer
    permission_classes = tuple()'''