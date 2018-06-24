from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'mpatrol'

router = DefaultRouter()
router.register('player', api.PlayerViewSet, base_name='player')
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