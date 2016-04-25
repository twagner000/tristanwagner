from django.conf.urls import url
from . import views
from .views import PuzzleDetail

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^p/(?P<slug>[\w-]+)/$', PuzzleDetail.as_view(), name='detail'),
]
