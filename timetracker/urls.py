from django.conf.urls import url
from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'timetracker'

router = SimpleRouter()
router.register('api/entry', views.EntryViewSet)
router.register('api/task', views.TaskViewSet)

urlpatterns = router.urls + [
    re_path('^(?!api).*$', views.IndexView.as_view(), name='index'),
]
