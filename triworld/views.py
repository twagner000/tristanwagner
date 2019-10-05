from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from . import models


class FaceView(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'triworld/face.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['mjtri'] = models.MajorTri.objects.filter(world=8, face_ring=1, face_index=0)
        
        return context
        
        
class NewWorldView(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'triworld/new_world.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        new_world = models.World()
        new_world.save()
        n = new_world.major_dim
        
        mjtri = []
        for face_ring in range(4):
            for face_index in range(5):
                for mjrow in range(n):
                    for mjcol in range(2*n-1):
                        if 2*mjrow+mjcol>2*n-2:
                            continue
                            
                        sea = True
                        
                        #polar caps
                        if face_ring in (0,3) and mjrow>=n-(n//3):
                            sea = False
                        
                        #home continent
                        if face_ring==1 and face_index==0:
                            if 2*mjrow+mjcol>2*(n//3)-2 and mjcol<2*n-2*(n//3) and mjrow<n-(n//3):
                                sea = False
                        
                        mjtri.append(models.MajorTri(
                            world=new_world,
                            face_ring=face_ring,
                            face_index=face_index,
                            major_row=mjrow,
                            major_col=mjcol,
                            sea=sea,
                            ))
        models.MajorTri.objects.bulk_create(mjtri)

        context['new_world'] = new_world
        context['mjtri_count'] = new_world.majortri_set.all().count()
        
        return context