from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'bg_rec'

router = SimpleRouter()
router.register('api/game', views.BoardGameViewSet)

urlpatterns = router.urls + [
    re_path('^(?!api).*$', TemplateView.as_view(template_name="bg_rec/index.html"), name='index'),
    path('api/unpickle', views.UnpickleView.as_view(), name='unpickle'),
]