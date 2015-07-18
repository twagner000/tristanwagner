from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'games.views.index', name='index'),
)
