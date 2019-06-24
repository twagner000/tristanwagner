from django.conf.urls import url
from . import views

app_name = 'timetracker'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^api/play$', views.PlayList.as_view(), name='api-play-list'),    
]
