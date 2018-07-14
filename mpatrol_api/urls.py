from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework_extensions.routers import ExtendedDefaultRouter
#NEED TO UPDATE rest_framework_extensions/routers.py FROM GITHUB

from . import api

app_name = 'mpatrol_api'
router = ExtendedDefaultRouter()
game = router.register('game', api.GameViewSet, base_name='game')
game.register('player', api.PublicPlayerViewSet, base_name='game-player', parents_query_lookups=['game_id'])
game.register('top5', api.Top5PlayerViewSet, base_name='game-top5', parents_query_lookups=['game_id'])
player = router.register('player', api.PlayerViewSet, base_name='player')
player.register('battalion', api.BattalionViewSet, base_name='player-battalion', parents_query_lookups=['player_id'])
player.register('log', api.PlayerLogViewSet, base_name='player-log', parents_query_lookups=['player_id'])
router.register('leaderlevel', api.LeaderLevelViewSet)
router.register('technology', api.TechnologyViewSet)
router.register('structure', api.StructureViewSet)
router.register('creature', api.CreatureViewSet)
router.register('weapon_base', api.WeaponBaseViewSet)
router.register('weapon_material', api.WeaponMaterialViewSet)
router.register('auth-token',api.AuthTokenViewSet, base_name='auth-token')

urlpatterns = router.urls