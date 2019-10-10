from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from . import serializers, models

class WorldViewSet(NestedViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.World.objects.all()
    serializer_class = serializers.WorldSerializer
    
    def create(self, request, *args, **kwargs):
        new_world = models.World()
        new_world.save()
        n = new_world.major_dim
        
        mjtri = []
        for face_ring in range(4):
            for face_index in range(5):
                face = models.Face(world=new_world, face_ring=face_ring, face_index=face_index)
                face.save()
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
                            face=face,
                            major_row=mjrow,
                            major_col=mjcol,
                            sea=sea,
                            ))
        models.MajorTri.objects.bulk_create(mjtri)
                
        return Response(serializers.WorldSerializer(new_world).data)
        
        
class FaceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.Face.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.FaceSerializer
        else:
            return serializers.BriefFaceSerializer
            
    @action(detail=True)
    def clear_cache(self, request, pk=None):
        self.get_object().clear_cache()
        print('cache cleared')
        return Response({'status': 'cache cleared'})
            
"""            
class FaceView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = models.Face.objects.all()
    serializer_class = serializers.FaceSerializer
    
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in ('world__pk','face_ring','face_index'):
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
"""