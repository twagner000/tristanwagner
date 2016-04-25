from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<checklist_id>\d+)/take/$', views.take, name='take'),
    url(r'^(?P<checklist_id>\d+)/history/$', views.history, name='history'),
    url(r'^(?P<ans_checklist_id>\d+)/results/$', views.results, name='results'),
    url(r'^(?P<checklist_id>\d+)/submit/$', views.submit, name='submit'),
]
