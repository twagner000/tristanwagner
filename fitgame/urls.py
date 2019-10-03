from django.urls import path, re_path
from django.views.generic import TemplateView
#from rest_framework.routers import SimpleRouter
from . import views

app_name = 'fitgame'

#router = SimpleRouter()
#router.register('api/game', views.BoardGameViewSet)

#urlpatterns = router.urls + [
urlpatterns = [
    #re_path('^(?!api).*$', TemplateView.as_view(template_name="bg_rec/index.html"), name='index'),
    path('', TemplateView.as_view(template_name="fitgame/index.html"), name='index'),
    
    # OAuth authentication
    path('login/', views.login, name='fitbit-login'),
    path('complete/', views.complete, name='fitbit-complete'),
    path('error/', TemplateView.as_view(template_name="fitgame/error.html"), name='fitbit-error'),
    path('logout/', views.logout, name='fitbit-logout'),

    # Fitbit data retrieval
    path('get_steps/', views.get_steps, name='fitbit-steps')
]