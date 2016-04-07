from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'puzzles.views.index', name='index'),
)
