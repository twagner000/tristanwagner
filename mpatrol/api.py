from django.core.exceptions import PermissionDenied
from django.conf import settings
from rest_framework import generics, viewsets, views, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

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


class WeaponBaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WeaponBase.objects.all()
    serializer_class = serializers.WeaponBaseSerializer


class WeaponMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WeaponMaterial.objects.all()
    serializer_class = serializers.WeaponMaterialSerializer
    
    
class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PlayerSerializer
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if settings.DEBUG:
            return models.Player.objects.filter(game__ended_date__isnull=True)
        return models.Player.objects.filter(user=self.request.user, game__ended_date__isnull=True)
        
    @action(methods=['post'], detail=True)
    def upgrade(self, request, pk=None):
        player = self.get_object()
        serializer = serializers.PlayerUpgradeSerializer(player, data=request.data)
        if serializer.is_valid():
            up_opj = serializer.validated_data['upgrade_obj']
            if serializer.validated_data['upgrade_type'] == 'leaderlevel':
                player.xp = player.xp - up_opj.cost_xp
                player.ll = up_opj
                player.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            if serializer.validated_data['upgrade_type'] == 'structure':
                player.xp -= up_opj.cost_xp
                player.gold -= up_opj.cost_gold
                player.structures.add(up_opj)
                player.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            if serializer.validated_data['upgrade_type'] == 'technology':
                player.xp -= up_opj.cost_xp
                player.technologies.add(up_opj)
                player.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            