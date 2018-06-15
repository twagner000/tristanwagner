from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from . import api

app_name = 'mpatrol'

api_patterns = ([
    path('creature/', api.CreatureList.as_view(), name='creature-list'),
    path('technology/', api.TechnologyList.as_view(), name='technology-list'),
    path('technology/<int:pk>/', api.TechnologyDetail.as_view(), name='technology-detail'),
], 'api')

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('reference/', views.ReferenceView.as_view(), name='reference'),
    path('api/', include(api_patterns)),
]