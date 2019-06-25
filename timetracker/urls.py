from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'timetracker'

urlpatterns = [
    re_path('^$', views.IndexView.as_view(), name='index'),
    path('api/entry/', views.EntryListCreate.as_view(), name='entry-list'),
    path('api/entry/recent/', views.RecentEntryList.as_view(), name='recent-entry-list'),
]
