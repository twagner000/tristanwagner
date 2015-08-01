from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('',
    url(r'^$', views.TurnDetailView.as_view(), name='index'),
    url(r'^start/$', views.start, name='start'),
    url(r'^choose_open/$', views.choose_open, name='choose_open'),
    url(r'^crops/$', views.CropsUpdateView.as_view(), name='crops'),
    url(r'^budget/$', views.BudgetUpdateView.as_view(), name='budget'),
    url(r'^debt/$', views.DebtUpdateView.as_view(), name='debt'),
    url(r'^endturn/$', views.EndTurnUpdateView.as_view(), name='endturn'),
)
