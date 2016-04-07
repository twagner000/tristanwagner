from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'puzzles.views.index', name='index'),
    url(r'^solved/$', 'puzzles.views.solved', name='solved'),
    url(r'^wrong/$', 'puzzles.views.wrong', name='wrong'),
)
