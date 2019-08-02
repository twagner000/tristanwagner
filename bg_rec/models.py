from django.db import models

class BoardGame(models.Model):
    objectid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    yearpublished = models.IntegerField(null=True, blank=True)
    minplayers = models.IntegerField(null=True, blank=True)
    maxplayers = models.IntegerField(null=True, blank=True)
    minplaytime = models.IntegerField(null=True, blank=True)
    maxplaytime = models.IntegerField(null=True, blank=True)
    playingtime = models.IntegerField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)
    bayesaverage = models.FloatField(null=True, blank=True)
    usersrated = models.IntegerField(null=True, blank=True)
    averageweight = models.FloatField(null=True, blank=True)
    thumbnail = models.CharField(max_length=250, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return '{} ({})'.format(self.name,self.objectid)
        
    def bgg_link(self):
        return 'https://boardgamegeek.com/boardgame/{}/'.format(self.objectid)
    
    class Meta:
        ordering = ['name']
        
class GameFactors(models.Model):
    game = models.OneToOneField('BoardGame', on_delete=models.CASCADE)
    bias = models.FloatField(null=True, blank=True)
    factors_json = models.TextField(blank=True) #for json_data, use json.dumps(pyvar) or pyvar = json.loads(self.json_data)
    date_updated = models.DateTimeField(auto_now=True)
    
class GameNeighbor(models.Model):
    game = models.ForeignKey('BoardGame', on_delete=models.CASCADE)
    neighbor = models.ForeignKey('BoardGame', on_delete=models.CASCADE, related_name='gameneighbor_set_neighbors')
    rank = models.IntegerField()
    distance = models.FloatField()
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['game', 'rank']
    