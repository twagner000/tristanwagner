from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
import json

from . import models


class FaceMapView(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'triworld/face.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['mjtri'] = models.MajorTri.objects.filter(world=8, face_ring=1, face_index=0)
        
        return context