from django.core.exceptions import PermissionDenied
from rest_framework import generics

from .serializers import CreatureSerializer, TechnologySerializer, PlayerSerializer
from .models import Creature, Technology, Player


class CreatureList(generics.ListAPIView):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer


class CreatureDetail(generics.RetrieveAPIView):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer
    

class TechnologyList(generics.ListAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    

class TechnologyDetail(generics.RetrieveAPIView):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    
class PlayerDetail(generics.RetrieveAPIView):
    serializer_class = PlayerSerializer
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Player.objects.filter(pk=11)
            #raise PermissionDenied()
        return Player.objects.filter(user=self.request.user)
    
    def get_object(self):
        #return self.get_queryset().get(pk=self.request.session.get('mpatrol_player_pk', None))
        return self.get_queryset().get(pk=11)