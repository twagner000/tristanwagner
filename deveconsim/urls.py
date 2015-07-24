from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'deveconsim.views.index', name='index'),
)
