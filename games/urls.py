from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^findbggusers$', views.findbggusers),
    url(r'^userstoquery$', views.userstoquery),
    url(r'^getuserratings$', views.getuserratings),
)
