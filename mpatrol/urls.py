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
    path('api/', include(api_patterns)),
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('resume/', views.ResumeFormView.as_view(), name='resume'),
    path('join/', views.JoinFormView.as_view(), name='join'),
    path('reference/', views.ReferenceView.as_view(), name='reference'),
]