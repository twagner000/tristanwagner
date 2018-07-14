from django.urls import path
from . import views

app_name = 'mpatrol'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<ngpath>', views.IndexView.as_view()),
]