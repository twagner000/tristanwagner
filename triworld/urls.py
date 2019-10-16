from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework_extensions.routers import ExtendedDefaultRouter
#NEED TO UPDATE rest_framework_extensions/routers.py FROM GITHUB

from . import api
from . import views

app_name = 'triworld'

router = ExtendedDefaultRouter()
world = router.register('api/world', api.WorldViewSet, base_name='world')
world.register('mjtri', api.MajorTriViewSet, base_name='world-mjtri', parents_query_lookups=['face__world__id'])

urlpatterns = [
    re_path('^(?!api).*$', TemplateView.as_view(template_name="triworld/index.html"), name='index'),
] + router.urls