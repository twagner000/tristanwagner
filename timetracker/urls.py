from django.conf.urls import url
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter
from . import views

app_name = 'timetracker'

router = SimpleRouter()
router.register('api/entry', views.EntryViewSet)
router.register('api/task', views.TaskViewSet)
router.register('api/project', views.ProjectViewSet)

urlpatterns = router.urls + [
    re_path('^api/summary/(?P<period>\d{4}-\d{2}-\d{2}-to-\d{4}-\d{2}-\d{2})/', views.DateRangeProjectList.as_view()),
    re_path('^(?!api).*$', TemplateView.as_view(template_name='timetracker/index.html'), name='index'),
]
