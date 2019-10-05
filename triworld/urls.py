from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework_extensions.routers import ExtendedDefaultRouter
#NEED TO UPDATE rest_framework_extensions/routers.py FROM GITHUB

from . import api
from . import views

app_name = 'triworld'

router = ExtendedDefaultRouter()
world = router.register('api/world', api.WorldViewSet, base_name='world')
world.register('face', api.FaceViewSet, base_name='world-face', parents_query_lookups=['world_id'])
#player = router.register('player', api.PlayerViewSet, base_name='player')
#player.register('battalion', api.BattalionViewSet, base_name='player-battalion', parents_query_lookups=['player_id'])
#player.register('log', api.PlayerLogViewSet, base_name='player-log', parents_query_lookups=['player_id'])


urlpatterns = router.urls + [
    re_path('^(?!api).*$', TemplateView.as_view(template_name="triworld/index.html"), name='index'),
    path('api/new_world', views.NewWorldView.as_view(), name='new-world'),
    path('api/face', views.FaceMapView.as_view(), name='face'),
    path('api/world/<world__pk>/face/<face_ring>/<face_index>', api.FaceView.as_view(), name='world-face-detail'),
]