from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
#import accounts.views
from rest_framework.authtoken import views as rest_framework_views


urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, {'next_page':'home'}, name='logout'),
    path('accounts/token/', rest_framework_views.obtain_auth_token, name='auth-token'),
    path('checklist/', include(('checklist.urls', 'checklist'), namespace='checklist')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('puzzles/', include(('puzzles.urls', 'puzzles'), namespace='puzzles')),
    path('deveconsim/', include(('deveconsim.urls', 'deveconsim'), namespace='deveconsim')),
    path('mpatrol-api/', include('mpatrol_api.urls')),
    path('mpatrol/', include('mpatrol.urls', namespace='mpatrol')),
]