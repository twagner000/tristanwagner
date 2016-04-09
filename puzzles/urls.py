from django.conf.urls import patterns, url
from . import views
from .views import PuzzleDetail

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^p/(?P<slug>[\w-]+)/$', PuzzleDetail.as_view(), name='detail'),
)
