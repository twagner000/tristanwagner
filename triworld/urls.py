from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'triworld'

#router = SimpleRouter()
#router.register('api/game', views.BoardGameViewSet)

#urlpatterns = router.urls + [
urlpatterns = [
    re_path('^(?!api).*$', TemplateView.as_view(template_name="triworld/index.html"), name='index'),
    path('api/new_world', views.NewWorldView.as_view(), name='new-world'),
]