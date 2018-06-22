from django.core.exceptions import PermissionDenied
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

    
class PlayerUpgrade(views.APIView):
    #permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        player = models.Player.objects.get(pk=request.data.get('player_id', None))
        #if player.user != request.user:
        #    return Response({"success": False, "error": "Cannot upgrade another user's player."})
        print('add back user check')
        upgrade_type = request.data.get('upgrade_type', None)
        if upgrade_type == 'll':
            ll_upgrade = player.ll_upgrade()
            if not ll_upgrade:
                return Response({"success": False, "error": "No leader level upgrade currently available."})
            elif request.data.get('upgrade_id',None) != ll_upgrade.id:
                return Response({"success": False, "error": "Can currently only upgrade to level {0}.".format(ll_upgrade.level)})
            elif player.xp < ll_upgrade.xp_cost:
                return Response({"success": False, "error": "Insufficient XP."})
            else:
                player.xp = player.xp - ll_upgrade.xp_cost
                player.ll = ll_upgrade
                player.save()
                return Response({"success": True})
        if upgrade_type == 'structure':
            upgrade_list = player.structure_upgrade()
            if not upgrade_list:
                return Response({"success": False, "error": "No structures currently available/affordable."})
            elif (request.data.get('upgrade_id',None),) not in upgrade_list.values_list('pk'):
                return Response({"success": False, "error": "Invalid structure selection."})
            else:
                upgrade_obj = models.Structure.objects.get(pk=request.data.get('upgrade_id',None))
                player.xp -= upgrade_obj.cost_xp
                player.gold -= upgrade_obj.cost_gold
                player.structures.add(upgrade_obj)
                player.save()
                return Response({"success": True})
        if upgrade_type == 'technology':
            upgrade_list = player.technology_upgrade()
            if not upgrade_list:
                return Response({"success": False, "error": "No technologies currently available/affordable."})
            elif (request.data.get('upgrade_id',None),) not in upgrade_list.values_list('pk'):
                return Response({"success": False, "error": "Invalid technology selection."})
            else:
                upgrade_obj = models.Technology.objects.get(pk=request.data.get('upgrade_id',None))
                player.xp -= upgrade_obj.cost_xp
                player.technologies.add(upgrade_obj)
                player.save()
                return Response({"success": True})
        else:
            return Response({"success": False, "error": "Invalid upgrade type."})