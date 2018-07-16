from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views

from accounts.forms import CrispyAuthenticationForm

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CrispyAuthenticationForm), name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('accounts/token/', rest_framework_views.obtain_auth_token, name='auth-token'),
    #path('accounts/', include('registration.backends.hmac.urls')), #https://github.com/ubernostrum/django-registration/blob/master/docs/hmac.rst
    #accounts/password_change/ [name='password_change']
    #accounts/password_change/done/ [name='password_change_done']
    #accounts/password_reset/ [name='password_reset']
    #accounts/password_reset/done/ [name='password_reset_done']
    #accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #accounts/reset/done/ [name='password_reset_complete']
    path('checklist/', include(('checklist.urls', 'checklist'), namespace='checklist')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('puzzles/', include(('puzzles.urls', 'puzzles'), namespace='puzzles')),
    path('deveconsim/', include(('deveconsim.urls', 'deveconsim'), namespace='deveconsim')),
    path('mpatrol-api/', include('mpatrol_api.urls')),
    path('mpatrol/', include('mpatrol.urls', namespace='mpatrol')),
]