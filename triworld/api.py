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
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.WorldSerializer
        else:
            return serializers.BriefWorldSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.BriefWorldSerializer(data=request.data)
        if serializer.is_valid():
            world = models.World(major_dim=serializer.validated_data['major_dim'], minor_dim=serializer.validated_data['minor_dim'])
            world.save()
            
            models.Face.objects.bulk_create(models.Face(world=world, ring=ring, ring_i=ring_i) for ring in range(4) for ring_i in range(5))
            models.MajorTri.objects.bulk_create(models.MajorTri(face=face,i=i) for face in world.face_set.all() for i in range(world.major_dim**2))
            
            world.update_cache()
            world.add_continents()
                    
            return Response(serializers.BriefWorldSerializer(world).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True)
    def add_continents(self, request, pk=None):
        self.get_object().add_continents()
        return Response({'status': 'continents generated'})