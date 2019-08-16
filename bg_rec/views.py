import pickle

from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, viewsets
from django.conf import settings

from . import models
from . import serializers

class IndexView(TemplateView):
    template_name = 'bg_rec/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boardgames'] = models.BoardGame.objects.all()
        if self.request.GET.get('id'):
            context['match'] = models.BoardGame.objects.get(pk=self.request.GET.get('id'))
        return context
    
class BoardGameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.BoardGame.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.BoardGameSearchSerializer
        else:
            return serializers.BriefBoardGameSerializer

class UnpickleView(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'bg_rec/unpickle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open(str(settings.APPS_DIR.path('boardgames.pkl')),'rb') as f:
            boardgames = pickle.load(f)
        
        batch = int(self.request.GET.get('batch',0))
        print('batch={}'.format(batch))
        batchsize = 250
        
        if batch <= 1:
            bulk_factors = []
            for game in boardgames:
                game_dict = dict((f.name,game[f.name]) for f in models.BoardGame._meta.get_fields() if f.name in game)
                game_obj, created = models.BoardGame.objects.get_or_create(**game_dict)
                game_obj.save()
                new_factors = models.GameFactors(game=game_obj, bias=game['bias'], factors_json=game['factors_json'])
                bulk_factors.append(new_factors)
            n_factors_del, _ = models.GameFactors.objects.all().delete()
            models.GameFactors.objects.bulk_create(bulk_factors)
            context['n_boardgame'] = len(boardgames)
            context['n_gamefactors'] = len(bulk_factors)

        if batch > 1:
            start, end = ((batch-2)*batchsize, (batch-1)*batchsize)
        elif batch == 1:
            start, end = (0,0)
        else:
            start, end = (0,None)
            
        bulk_neighbors = []
        for game in boardgames[start:end]:
            for rank_zero, (neighbor_id, distance) in enumerate(game['neighbors']):
                try:
                    neighbor = models.BoardGame.objects.get(pk=neighbor_id)
                    neighbor_obj = models.GameNeighbor(
                        game=models.BoardGame.objects.get(pk=game['objectid']),
                        neighbor=neighbor,
                        rank=rank_zero+1,
                        distance=distance)
                    bulk_neighbors.append(neighbor_obj)
                except ObjectDoesNotExist:
                    pass #print("Couldn't find id [{}].".format(neighbor_id))
        n_neighbors_del, _ = models.GameNeighbor.objects.filter(game__in=[g['objectid'] for g in boardgames[start:end]]).delete()
        models.GameNeighbor.objects.bulk_create(bulk_neighbors)
        context['n_gameneighbor'] = len(bulk_neighbors)
        return context