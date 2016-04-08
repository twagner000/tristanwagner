from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^p/(?P<slug>[\w-]+)/check/$', views.check, name='check'),
    url(r'^p/(?P<slug>[\w-]+)/$', views.puzzle_detail, name='detail'),
)
