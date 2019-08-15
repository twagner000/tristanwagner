from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'bg_rec'

router = SimpleRouter()
router.register('api/game', views.BoardGameViewSet)

urlpatterns = router.urls + [
    #path('', views.IndexView.as_view(), name='index'),
    re_path('^(?!api).*$', TemplateView.as_view(template_name="pages/bg_rec.html"), name='index'),
    path('api/unpickle', views.UnpickleView.as_view(), name='unpickle'),
]