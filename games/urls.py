from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^findbggusers$', views.findbggusers),
    #url(r'^userstoquery$', views.userstoquery),
    #url(r'^getuserratings$', views.getuserratings),
    #url(r'^populate_play_dates$', views.populate_play_dates),
    url(r'^api/play$', views.PlayList.as_view(), name='api-play-list'),
    #url(r'^api/dates$', views.PlayDateList.as_view()),
]
