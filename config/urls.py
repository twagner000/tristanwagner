from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views

from accounts.forms import CrispyAuthenticationForm, CrispyPasswordChangeForm

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/token/', rest_framework_views.obtain_auth_token, name='auth-token'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CrispyAuthenticationForm), name='login'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(form_class=CrispyPasswordChangeForm), name='password_change'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('accounts/', include('registration.backends.hmac.urls')), #https://github.com/ubernostrum/django-registration/blob/master/docs/hmac.rst
    path('accounts/', include('django.contrib.auth.urls')),
    path('checklist/', include(('checklist.urls', 'checklist'), namespace='checklist')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('puzzles/', include(('puzzles.urls', 'puzzles'), namespace='puzzles')),
    path('deveconsim/', include(('deveconsim.urls', 'deveconsim'), namespace='deveconsim')),
    path('mpatrol-api/', include('mpatrol_api.urls')),
    path('mpatrol/', include('mpatrol.urls', namespace='mpatrol')),
]