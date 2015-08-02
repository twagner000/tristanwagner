from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = patterns('',
    url(r'^$', views.TurnDetailView.as_view(), name='index'),
    url(r'^start/$', views.GameFormView.as_view(), name='start'),
    url(r'^crops/$', views.CropsUpdateView.as_view(), name='crops'),
    url(r'^budget/$', views.BudgetUpdateView.as_view(), name='budget'),
    url(r'^debt/$', views.DebtUpdateView.as_view(), name='debt'),
    url(r'^endturn/$', views.EndTurnUpdateView.as_view(), name='endturn'),
    url(r'^voted_out/(?P<pk>[0-9]+)/$', views.VotedOutView.as_view(), name='voted_out'),
)
