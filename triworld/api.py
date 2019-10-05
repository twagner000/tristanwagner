from rest_framework import viewsets, permissions, generics
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.shortcuts import get_object_or_404

from . import serializers, models

class WorldViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.World.objects.all()
    serializer_class = serializers.WorldSerializer
        
class FaceViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = models.Face.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.FaceSerializer
        else:
            return serializers.BriefFaceSerializer
            
            
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
        
"""    def get_queryset(self):
        return models.Player.objects.filter(user=self.request.user, game__ended_date__isnull=True)
        
    def retrieve(self, request, pk=None):
        player = self.get_object()
        now = constants.pacific.localize(datetime.datetime.now())
        if not player.score_last_updated or (now - player.score_last_updated) > constants.refresh_score_timedelta:
            player.score_last_updated = now #dummy value to trigger refresh in model save()
            player.save()
        return super().retrieve(request,pk)"""