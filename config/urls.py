from django.urls import include, path
from django.contrib import admin
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as rest_framework_views
#NEED TO UPDATE rest_framework_extensions/routers.py FROM GITHUB
from rest_framework_extensions.routers import ExtendedDefaultRouter

from accounts.api import AuthTokenViewSet


from accounts.forms import CrispyAuthenticationForm, CrispyPasswordChangeForm, CrispyPasswordResetForm, CrispySetPasswordForm

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('blog/', TemplateView.as_view(template_name='pages/blog.html'), name='blog'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('attribution/', TemplateView.as_view(template_name='pages/attribution.html'), name='attribution'),
    path('admin/', admin.site.urls),
    path('accounts/token/', rest_framework_views.obtain_auth_token, name='auth-token'),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=CrispyAuthenticationForm), name='login'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(form_class=CrispyPasswordChangeForm), name='password_change'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=CrispyPasswordResetForm), name='password_reset'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CrispySetPasswordForm), name='password_reset_confirm'),
    #path('accounts/', include('registration.backends.hmac.urls')), #https://github.com/ubernostrum/django-registration/blob/master/docs/hmac.rst
    path('accounts/', include('django.contrib.auth.urls')),
    path('checklist/', include(('checklist.urls', 'checklist'), namespace='checklist')),
    path('bgg-stats/', include('bgg_stats.urls')),
    path('puzzles/', include(('puzzles.urls', 'puzzles'), namespace='puzzles')),
    path('deveconsim/', include(('deveconsim.urls', 'deveconsim'), namespace='deveconsim')),
    path('mpatrol-api/', include('mpatrol_api.urls')),
    path('mpatrol/', include('mpatrol.urls', namespace='mpatrol')),
    path('timetracker/', include('timetracker.urls')),
    path('bg_rec/', include('bg_rec.urls')),
    path('fitgame/', include('fitgame.urls')),
    path('triworld/', include('triworld.urls')),
]

router = ExtendedDefaultRouter()
router.register('accounts/auth-token',AuthTokenViewSet, base_name='auth-token')
urlpatterns += router.urls