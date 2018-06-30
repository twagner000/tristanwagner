from django.core.exceptions import PermissionDenied
from django.conf import settings
from rest_framework import generics, viewsets, views, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin
from datetime import datetime
import random
import json

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


class BattalionViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Battalion.objects.all()
    serializer_class = serializers.BattalionSerializer
    lookup_field = 'battalion_number'
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        q = super().get_queryset()
        if settings.DEBUG:
            return q.filter(player__game__ended_date__isnull=True)
        return q.filter(player__user=self.request.user, player__game__ended_date__isnull=True)
        
    @action(methods=['post'], detail=True)
    def hire(self, request, parent_lookup_player_id, battalion_number):
        battalion = self.get_object()
        request.data.update({'action':'hire'})
        serializer = serializers.BattalionUpdateSerializer(battalion, data=request.data)
        if serializer.is_valid():
            if not battalion.count: #make sure other fields are reset if this is a new battalion
                battalion.creature = serializer.validated_data['creature']
                battalion.level = 1
                battalion.weapon_base = None
                battalion.weapon_material = None
            battalion.count += serializer.validated_data['count_delta']
            battalion.player.gold -= serializer.validated_data['count_delta']*battalion.cost_gold(serializer.validated_data['creature'])
            battalion.player.xp -= serializer.validated_data['count_delta']*battalion.cost_xp()
            battalion.player.save()
            battalion.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=True)
    def train(self, request, parent_lookup_player_id, battalion_number):
        battalion = self.get_object()
        request.data.update({'action':'train'})
        serializer = serializers.BattalionUpdateSerializer(battalion, data=request.data)
        if serializer.is_valid():
            battalion.player.xp -= serializer.validated_data['cost_xp']
            battalion.level = serializer.validated_data['level']
            battalion.player.save()
            battalion.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['post'], detail=True)
    def arm(self, request, parent_lookup_player_id, battalion_number):
        battalion = self.get_object()
        request.data.update({'action':'arm'})
        serializer = serializers.BattalionUpdateSerializer(battalion, data=request.data)
        if serializer.is_valid():
            battalion.player.gold -= serializer.validated_data['cost_gold']
            battalion.weapon_base = serializer.validated_data['weapon_base']
            battalion.weapon_material = serializer.validated_data['weapon_material']
            battalion.player.save()
            battalion.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class GameViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Game.objects.filter(ended_date__isnull=True)
    serializer_class = serializers.BriefGameSerializer
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
        
        
class PublicPlayerViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PublicPlayerSerializer
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
        
        
class Top5PlayerViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerScoreSerializer
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().order_by('-static_score')[:5]
        
        
class PlayerLogViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.PlayerLog.objects.all()
    serializer_class = serializers.PlayerLogSerializer
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        q = super().get_queryset()
        if settings.DEBUG:
            return q.filter(player__game__ended_date__isnull=True)
        return q.filter(player__user=self.request.user, player__game__ended_date__isnull=True)
            
            
class PlayerViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PlayerSerializer
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if settings.DEBUG:
            return models.Player.objects.filter(game__ended_date__isnull=True)
        return models.Player.objects.filter(user=self.request.user, game__ended_date__isnull=True)
        
    @action(methods=['post'], detail=True)
    def work(self, request, pk=None):
        player = self.get_object()
        serializer = serializers.PlayerActionSerializer(player, data=request.data)
        if serializer.is_valid():
            calc = player.calc()
            player.gold += calc['work_gold']
            player.xp += calc['work_xp']
            msg = 'You worked for one day and earned {0} gold and {1} xp. You will not be able to attack or earn money again this turn.'.format(calc['work_gold'],calc['work_xp'])
            log = models.PlayerLog(player=player, action='work', action_points=1, description=msg)
            player.save()
            log.save()
            return Response({'message':msg}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['post'], detail=True)
    def spy(self, request, pk=None):
        player = self.get_object()
        serializer = serializers.PlayerActionSerializer(player, data=request.data)
        if serializer.is_valid():
            target_player = serializer.validated_data['target_player']
            calc = target_player.calc()
            json_data = {'discovered': False}
            msg = "<p>Your spies have reported back with the following information on {0}:</p><ul>".format(target_player.character_name)
            msg += "<li>This Patrol Master has {0} creatures in their patrol.</li>".format(sum(b.count for b in target_player.battalions.all()))
            if random.random() < 0.5:
                json_data['work_gold'] = calc['work_gold']
                msg += "<li>This Patrol Master earns {0} gold per turn.</li>".format(calc['work_gold'])
            if random.random() < 0.5:
                json_data['work_xp'] = calc['work_xp']
                msg += "<li>This Patrol Master earns {0} experience per turn.</li>".format(calc['work_xp'])
            if random.random() < 0.33:
                json_data['ll__level'] = target_player.ll.level
                msg += "<li>This Patrol Master has a leader level of {0}.</li>".format(target_player.ll.level)
            if random.random() < 0.33:
                json_data['attack'] = calc['attack']
                msg += "<li>This Patrol Master has an attack rating of {0}.</li>".format(round(calc['attack'],1))
            if random.random() < 0.33:
                json_data['defense'] = calc['defense']
                msg += "<li>This Patrol Master has a defense rating of {0}.</li>".format(round(calc['defense'],1))
            msg += "</ul>"
            if random.random() < 0.25:
                json_data['discovered'] = True
                msg += "<p>Sir! We have also received word from the spy that our espionage activities were discovered!</p>"
                msg2 = "<p>{0} has spied on you, sir. They came away with information on our numbers. Attack rating, defense rating, or other data may also be missing.</p>".format(player.character_name)
                log2 = models.PlayerLog(player=target_player, action='spied-on', action_points=0, description=msg2, target_player=player, json_data=json.dumps(json_data), acknowledged=False)
                log2.save()
            log = models.PlayerLog(player=player, action='spy', action_points=1, description=msg, target_player=target_player, json_data=json.dumps(json_data), success=not json_data['discovered'])
            log.save()
            return Response({'message':msg}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    @action(methods=['post'], detail=True)
    def attack(self, request, pk=None):
        player = self.get_object()
        serializer = serializers.PlayerActionSerializer(player, data=request.data)
        if serializer.is_valid():
            target_player = serializer.validated_data['target_player']
            ranfac = lambda:.9+.2*random.random()
            contestants = [player, target_player]
            life = [p.ll.life for p in contestants]
            calc = [p.calc() for p in contestants]
            msg = ""
            battle = []
            for turn in range(200):
                if min(life) <= 0:
                    break
                attack = round(calc[turn%2]['attack'] * ranfac(),0)
                defense = round(calc[turn%2+1]['defense'] * ranfac(),0)
                damage = min(life[turn%2+1],max(1,attack-defense)) #always do at least 1 damage
                life[turn%2+1] -= damage
                battle.append({
                    'leader':contestants[turn%2].character_name,
                    'action':'Attack',
                    'attack':attack,
                    'blocked':min(defense,attack-1),
                    'damage': damage,
                    'attacker_life': life[0],
                    'defender_life': life[1]
                    })
                print(battle[-1])
            
            if life[1] <= 0:
                winner, loser = contestants[0],contestants[1]
                wlife, llife = life[0], life[1]
            else:
                winner,loser = contestants[1], contestants[0]
                wlife, llife = life[1], life[0]
            xp_won = random.randint(1,1000) #only winner gains xp
            gold_won = max(0,loser.gold - loser.ll.level*100) #loser keeps 100 gold per leader level; winner steals the rest
            winner_troop_retain_ratio = .5 + wlife/(2*winner.ll.life) #take % life lost and lose half that many troops
            loser_troop_retain_ratio = .5
            
            msg += "<p>Winner: {0}".format(winner.character_name)
            msg += "<p>Experience: {0}</p>".format(xp_won)
            msg += "<p>Gold: {0}</p>".format(xp_won)
            msg += "<p>The winner has lost {0}% of their troops.</p>".format(100*(1-winner_troop_retain_ratio))
            msg += "<p>The loser has lost 50% of their troops.</p>"
    
            #newfile2 = newfile2 + "\nMessage "+int(messages+1)+" (Sender/Date/Subject/Status/Message): Mossflower HQ/"+szday+", "+year+" A.F./"+usrname+" Has Attacked You and Won!/Unread/"+replace(replace("<p align='center'>You have lost a battle to "+usrname+". You lost "+gwon+" Gold and the following troops: </p>"+troopslost+"<p align='center'>They have lost: </p>"+troopslostw+"<p align='center'>Here is a table with the battle stats: </p>"+battletable$, "/", "!(s)")$, "\"", "'")$
            
            return Response({'message':msg}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
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
            