from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^findbggusers$', views.findbggusers),
    url(r'^userstoquery$', views.userstoquery),
    url(r'^getuserratings$', views.getuserratings),
    url(r'^plays$', views.plays),
]
