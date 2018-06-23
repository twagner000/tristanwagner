from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'mpatrol'

router = DefaultRouter()
router.register('leaderlevel', api.LeaderLevelViewSet)
router.register('technology', api.TechnologyViewSet)
router.register('structure', api.StructureViewSet)
router.register('creature', api.CreatureViewSet)
api_patterns = router.urls

api_patterns = (api_patterns + [
    path('player/', api.PlayerDetail.as_view(), name='player-detail'),
    path('upgrade/', api.PlayerUpgrade.as_view(), name='upgrade'),
], 'api')

urlpatterns = [
    path('api/', include(api_patterns)),
    path('', views.IndexView.as_view(), name='index'),
    path('a', views.HomeView.as_view(), name='home'),
    path('resume/', views.ResumeFormView.as_view(), name='resume'),
    path('join/', views.JoinFormView.as_view(), name='join'),
    path('reference/', views.ReferenceView.as_view(), name='reference'),
]