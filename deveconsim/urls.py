from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^start/$', login_required(views.start), name='start'),
    url(r'^choose_open/$', login_required(views.choose_open), name='choose_open'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^start/$', views.start, name='start'),
    #url(r'^choose_open/$', views.choose_open, name='choose_open'),
)
