from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import generics, viewsets, views, mixins, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import datetime
import random
import json
import sys

from . import serializers, models, constants

class AuthTokenViewSet(viewsets.ViewSet):
    authentication_classes = (authentication.SessionAuthentication,)
    
    def list(self, request, format=None):
        token, created = Token.objects.get_or_create(user=self.request.user)
        return Response({'token': token.key})
        
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}) 
        return Response()
        
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    
class LeaderLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.LeaderLevel.objects.all()
    serializer_class = serializers.LeaderLevelSerializer
    permission_classes = [permissions.AllowAny]
        

class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Technology.objects.all()
    serializer_class = serializers.TechnologySerializer
    permission_classes = [permissions.AllowAny]

    
class StructureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    permission_classes = [permissions.AllowAny]


class CreatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Creature.objects.all()
    serializer_class = serializers.CreatureSerializer
    permission_classes = [permissions.AllowAny]


class WeaponBaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WeaponBase.objects.all()
    serializer_class = serializers.WeaponBaseSerializer
    permission_classes = [permissions.AllowAny]


class WeaponMaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WeaponMaterial.objects.all()
    serializer_class = serializers.WeaponMaterialSerializer
    permission_classes = [permissions.AllowAny]


class BattalionViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Battalion.objects.all()
    serializer_class = serializers.BattalionSerializer
    lookup_field = 'battalion_number'
    
    def get_queryset(self):
        q = super().get_queryset()
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
    def fire(self, request, parent_lookup_player_id, battalion_number):
        battalion = self.get_object()
        request.data.update({'action':'fire'})
        serializer = serializers.BattalionUpdateSerializer(battalion, data=request.data)
        if serializer.is_valid():
            battalion.player.gold += serializer.validated_data['count_delta']*battalion.refund_gold()
            battalion.count -= serializer.validated_data['count_delta']
            if not battalion.count: #make sure other fields are reset if firing entire battalion
                battalion.creature = None
                battalion.level = 1
                battalion.weapon_base = None
                battalion.weapon_material = None
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
    serializer_class = serializers.GamePlayerSerializer
        
class PublicPlayerViewSet(NestedViewSetMixin, mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PublicPlayerSerializer
        
    def create(self, request, parent_lookup_game_id):
        user = self.request.user #if not settings.DEBUG else models.Player.objects.filter(user__username='tristan').first().user
        request.data.update({'game':parent_lookup_game_id}) #models.Game.objects.get(id=parent_lookup_game_id)
        
        print(request.data)
        serializer = serializers.PublicPlayerSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            p = models.Player(game=serializer.validated_data['game'], user=user, character_name=serializer.validated_data['character_name'])
            p.save()
            for i in range(1,9):
                p.battalions.create(battalion_number=i)
            p.save()
            msg = 'Successfully joined game {0}'.format(p.game)
            return Response({'message':msg, 'player_id':p.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Top5PlayerViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerScoreSerializer
    
    def get_queryset(self):
        q = super().get_queryset().order_by('-static_score')
        n = q.count()
        cut = 5
        while n > cut and q[cut].static_score == q[cut-1].static_score:
            cut += 1
        return q[:cut]
        
        
class PlayerLogViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.PlayerLog.objects.all()
    serializer_class = serializers.PlayerLogSerializer
    
    def get_queryset(self):
        q = super().get_queryset()
        return q.filter(player__user=self.request.user, player__game__ended_date__isnull=True)
            
            
class PlayerViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PlayerSerializer
    
    def get_queryset(self):
        return models.Player.objects.filter(user=self.request.user, game__ended_date__isnull=True)
        
    def retrieve(self, request, pk=None):
        player = self.get_object()
        now = constants.pacific.localize(datetime.datetime.now())
        if not player.score_last_updated or (now - constants.pacific.localize(player.score_last_updated)) > constants.refresh_score_timedelta:
            player.score_last_updated = now #dummy value to trigger refresh in model save()
            player.save()
        return super().retrieve(request,pk)
        
    @action(methods=['post'], detail=True)
    def work(self, request, pk=None):
        player = self.get_object()
        serializer = serializers.PlayerActionSerializer(player, data=request.data)
        if serializer.is_valid():
            calc = player.calc()
            player.gold += calc['work_gold']
            player.xp += calc['work_xp']
            msg = 'You worked for one day and earned {0} gold and {1} xp. You will not be able to attack or earn money again this turn.'.format(calc['work_gold'],calc['work_xp'])
            json_data = {'work_gold':calc['work_gold'], 'work_xp':calc['work_xp']}
            log = models.PlayerLog(player=player, action='work', action_points=1, description=msg, json_data=json.dumps(json_data))
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
            json_data = {'discovered': False, 'num_creatures':sum(b.count for b in target_player.battalions.all())}
            msg = "<p>Your spies have reported back with the following information on {0}:</p><ul>".format(target_player.character_name)
            msg += "<li>This Patrol Master has {0} creatures in their patrol.</li>".format(json_data['num_creatures'])
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
            battle = []
            for turn in range(200):
                if min(life) <= 0:
                    break
                attack = int(calc[turn%2]['attack'] * ranfac())
                defense = int(calc[(turn+1)%2]['defense'] * ranfac())
                damage = min(life[(turn+1)%2],max(1,attack-defense)) #always do at least 1 damage
                life[(turn+1)%2] -= damage
                battle.append({
                    'leader':contestants[turn%2].character_name,
                    'action':'Attack',
                    'attack':attack,
                    'blocked':min(defense,attack-1),
                    'damage': damage,
                    'attacker_life': life[0],
                    'defender_life': life[1]
                    })
            if min(life) <= 0:
                winner_index = 0 if life[1] <= 0 else 1
                winner, loser = contestants[winner_index],contestants[1-winner_index]
                xp_won = random.randint(1,1000) #only winner gains xp
                gold_won = max(0,loser.gold - loser.ll.level*100) #loser keeps 100 gold per leader level; winner steals the rest
                winner_troop_retain_ratio = .5 + life[winner_index]/(2*winner.ll.life) #take % life lost and lose half that many troops
                winner_troops = []
                loser_troops = []
                winner.xp += xp_won
                winner.gold += gold_won
                loser.gold -= gold_won
                for b in winner.battalions.filter(count__gt=0):
                    new_count = max(1,int(round(b.count*winner_troop_retain_ratio,0)))
                    winner_troops.append({'battalion_number': b.battalion_number, 'creature_id': b.creature.id if b.creature else None, 'creature_name': b.creature.name if b.creature else None, 'initial_count':b.count, 'final_count':new_count})
                    b.count = new_count
                    b.save()
                    print("{0} battalion {1} count={2}".format(winner.character_name,b.battalion_number,b.count))
                for b in loser.battalions.filter(count__gt=0):
                    new_count = max(1,int(round(b.count*.5,0)))
                    loser_troops.append({'battalion_number': b.battalion_number, 'creature_id': b.creature.id if b.creature else None, 'creature_name': b.creature.name if b.creature else None, 'initial_count':b.count, 'final_count':new_count})
                    b.count = new_count
                    b.save()
                    print("{0} battalion {1} count={2}".format(winner.character_name,b.battalion_number,b.count))
                json_data = {'battle': battle, 'attacker_id': player.id, 'xp_won': xp_won, 'gold_won': gold_won,
                            'winner_id': winner.id, 'winner_character_name': winner.character_name, 'winner_life': life[winner_index], 'winner_attack':calc[winner_index]['attack'], 'winner_defense':calc[winner_index]['defense'], 'winner_troops':winner_troops,
                            'loser_id': loser.id, 'loser_character_name': loser.character_name, 'loser_life': life[1-winner_index], 'loser_attack':calc[1-winner_index]['attack'], 'loser_defense':calc[1-winner_index]['defense'], 'loser_troops':loser_troops}
                common_msg = "<p>{0} ended the battle with {1} life remaining; {2} ended with {3} life remaining.".format(winner.character_name,life[winner_index],loser.character_name,life[1-winner_index])
                common_msg += "<p>{0} gained {1} experience and {2} gold, with {3}% troop attrition. {4} lost {2} gold with 50% troop attrition.</p>".format(winner.character_name, xp_won, gold_won, round(100*(1-winner_troop_retain_ratio),1), loser.character_name)
                common_msg += "<p>{0} lost the following troops: {1}.</p>".format(winner.character_name,", ".join(["{0} {1}".format((b['initial_count']-b['final_count']),b['creature_name']) for b in winner_troops]))
                common_msg += "<p>{0} lost the following troops: {1}.</p>".format(loser.character_name,", ".join(["{0} {1}".format((b['initial_count']-b['final_count']),b['creature_name']) for b in loser_troops]))
                msg = "<p>You attacked {0} and {1}!<p>".format(target_player.character_name,['won','lost'][winner_index])+common_msg
                msg2 = "<p>{0} attacked you and {1}!<p>".format(player.character_name,['won','lost'][winner_index])+common_msg
                log = models.PlayerLog(player=player, action='attack', action_points=1, description=msg, target_player=target_player, json_data=json.dumps(json_data), success=player==winner)
                log2 = models.PlayerLog(player=target_player, action='was-attacked', action_points=0, description=msg2, target_player=player, json_data=json.dumps(json_data), success=target_player==winner, acknowledged=False)
                log.save()
                log2.save()
                winner.save()
                loser.save()
            else:
                msg = "<p>The battle was a stalemate. Your daily action was not consumed.<p>"
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
            