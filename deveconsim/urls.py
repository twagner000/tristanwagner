from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^start/$', login_required(views.start), name='start'),
    url(r'^choose_open/$', login_required(views.choose_open), name='choose_open'),
    url(r'^crops/$', login_required(views.CropsView.as_view()), name='crops'),
    url(r'^budget/$', login_required(views.BudgetView.as_view()), name='budget'),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^start/$', views.start, name='start'),
    #url(r'^choose_open/$', views.choose_open, name='choose_open'),
)
