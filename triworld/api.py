from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions, generics, status
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
        serializer = serializers.WorldSerializer(data=request.data)
        if serializer.is_valid():
            world = models.World(major_dim=serializer.validated_data['major_dim'], minor_dim=serializer.validated_data['minor_dim'])
            world.save()
            n = world.major_dim
            
            mjtri = []
            for ring in range(4):
                for ring_i in range(5):
                    face = models.Face(world=world, ring=ring, ring_i=ring_i)
                    face.save()
                    fpd = face.fpd()
                    for mji in range(n*n):
                        sea = True
                            
                        #polar caps
                        if (ring==0 and mji<n*n//9) or (ring==3 and mji>=n*n*8//9):
                            sea = False
                        
                        #home continent
                        if ring==1 and ring_i==0:
                            ri,ci = models.MajorTri.static_rci(mji,n,fpd)
                            if 2*ri+ci>2*(n//3)-2 and ci<2*n-2*(n//3) and ri<n-(n//3):
                                sea = False
                        
                        mjtri.append(models.MajorTri(
                            face=face,
                            i=mji,
                            sea=sea,
                            ))
            models.MajorTri.objects.bulk_create(mjtri)
                    
            return Response(serializers.WorldSerializer(world).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
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