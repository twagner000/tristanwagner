from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tristanwagner.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'home'}, name='logout'),
    url(r'^checklist/', include('checklist.urls', namespace='checklist')),
    url(r'^games/', include('games.urls', namespace='games')),
    url(r'^deveconsim/', include('deveconsim.urls', namespace='deveconsim')),
)