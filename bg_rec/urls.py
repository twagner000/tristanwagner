from django.urls import path, re_path
from . import views

app_name = 'bg_rec'

urlpatterns = [
    #re_path('^api/summary/(?P<period>\d{4}-\d{2}-\d{2}-to-\d{4}-\d{2}-\d{2})/', views.DateRangeProjectList.as_view()),
    #re_path('^(?!api).*$', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('unpickle', views.UnpickleView.as_view(), name='unpickle'),
]
