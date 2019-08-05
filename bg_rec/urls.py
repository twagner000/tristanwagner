from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'bg_rec'

router = SimpleRouter()
router.register('api/game', views.BoardGameViewSet)

urlpatterns = router.urls + [
    path('', views.IndexView.as_view(), name='index'),
    #re_path('^(?!api).*$', views.IndexView.as_view(), name='index'),
    path('unpickle', views.UnpickleView.as_view(), name='unpickle'),
]