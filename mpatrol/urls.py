from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework_extensions.routers import ExtendedDefaultRouter
#NEED TO UPDATE rest_framework_extensions/routers.py FROM GITHUB

from . import views
from . import api

app_name = 'mpatrol'

router = ExtendedDefaultRouter()
player = router.register('player', api.PlayerViewSet, base_name='player')
player.register('battalion', api.BattalionViewSet, base_name='player-battalion', parents_query_lookups=['player_id'])
router.register('leaderlevel', api.LeaderLevelViewSet)
router.register('technology', api.TechnologyViewSet)
router.register('structure', api.StructureViewSet)
router.register('creature', api.CreatureViewSet)
router.register('weapon_base', api.WeaponBaseViewSet)
router.register('weapon_material', api.WeaponMaterialViewSet)

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    path('', views.IndexView.as_view(), name='index'),
    path('a', views.HomeView.as_view(), name='home'),
    path('resume/', views.ResumeFormView.as_view(), name='resume'),
    path('join/', views.JoinFormView.as_view(), name='join'),
    path('reference/', views.ReferenceView.as_view(), name='reference'),
]