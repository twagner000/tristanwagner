from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
import django.contrib.auth.views
admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page':'home'}, name='logout'),
    url(r'^checklist/', include('checklist.urls', namespace='checklist')),
    url(r'^games/', include('games.urls', namespace='games')),
    url(r'^puzzles/', include('puzzles.urls', namespace='puzzles')),
    url(r'^deveconsim/', include('deveconsim.urls', namespace='deveconsim')),
    url(r'^mpatrol/', include('mpatrol.urls', namespace='mpatrol')),
]