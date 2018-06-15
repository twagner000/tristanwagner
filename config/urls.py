from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView
import django.contrib.auth.views

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', django.contrib.auth.views.login, name='login'),
    path('accounts/logout/', django.contrib.auth.views.logout, {'next_page':'home'}, name='logout'),
    path('checklist/', include(('checklist.urls', 'checklist'), namespace='checklist')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('puzzles/', include(('puzzles.urls', 'puzzles'), namespace='puzzles')),
    path('deveconsim/', include(('deveconsim.urls', 'deveconsim'), namespace='deveconsim')),
    path('mpatrol/', include('mpatrol.urls')),
]