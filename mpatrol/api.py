from django.core.exceptions import PermissionDenied
from rest_framework import generics, viewsets

from . import serializers, models
    
    
class LeaderLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.LeaderLevel.objects.all()
    serializer_class = serializers.LeaderLevelSerializer
        

class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Technology.objects.all()
    serializer_class = serializers.TechnologySerializer

    
class StructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer


class CreatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Creature.objects.all()
    serializer_class = serializers.CreatureSerializer


class PlayerMixin(object):
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return models.Player.objects.filter(pk=11)
            #raise PermissionDenied()
        return models.Player.objects.filter(user=self.request.user)
    
    def get_object(self):
        #return self.get_queryset().get(pk=self.request.session.get('mpatrol_player_pk', None))
        return self.get_queryset().get(pk=11)


class PlayerDetail(PlayerMixin, generics.RetrieveAPIView):
    serializer_class = serializers.PlayerSerializer
        
        
class UpgradeLeaderLevel(PlayerMixin, generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UpgradeLeaderLevelSerializer
    