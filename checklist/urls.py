from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'checklist.views.index', name='index'),
    url(r'^(?P<checklist_id>\d+)/take/$', 'checklist.views.take', name='take'),
    url(r'^(?P<checklist_id>\d+)/history/$', 'checklist.views.history', name='history'),
    url(r'^(?P<ans_checklist_id>\d+)/results/$', 'checklist.views.results', name='results'),
    url(r'^(?P<checklist_id>\d+)/submit/$', 'checklist.views.submit', name='submit'),
)
