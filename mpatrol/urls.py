from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'mpatrol'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('reference/', views.ReferenceView.as_view(), name='reference'),
]
