from rest_framework import generics

from .serializers import CreatureSerializer, TechnologySerializer
from .models import Creature, Technology


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