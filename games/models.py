from django.db import models
from django.utils import timezone
import datetime

class BGGUserSearch(models.Model):
    q = models.CharField(max_length=50)
    users = models.TextField(blank=True)
    search_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.q
        
    def user_list(self):
        return self.users.split(',') if self.users else []

class BGGGame(models.Model):
    objectid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    yearpublished = models.IntegerField(null=True, blank=True)
    minplayers = models.IntegerField(null=True, blank=True)
    maxplayers = models.IntegerField(null=True, blank=True)
    minplaytime = models.IntegerField(null=True, blank=True)
    maxplaytime = models.IntegerField(null=True, blank=True)
    playingtime = models.IntegerField(null=True, blank=True)
    numowned = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return '%s (%d)' % (self.name,self.objectid)
    
class BGGUser(models.Model):
    user = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user
    
class BGGUserRating(models.Model):
    game = models.ForeignKey(BGGGame, on_delete=models.CASCADE)
    user = models.ForeignKey(BGGUser, on_delete=models.CASCADE)
    rating = models.FloatField()
    numplays = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

class BGGPlay(models.Model):
    bgg_play_id = models.IntegerField(primary_key=True)
    bgg_game_id = models.IntegerField(null=True, blank=True)
    game_name = models.CharField(max_length=250)
    date = models.DateTimeField(default=timezone.now)
    quantity = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date','game_name']
    
    def __str__(self):
        return '{0}: {1:%Y}-{1:%m}-{1:%d} {2}'.format(self.bgg_play_id, self.date, self.game_name)
        
class BGGPlayDate(models.Model):
    date = models.DateField(primary_key=True)
    
    class Meta:
        ordering = ['date']
        
    def plays(self):
        return BGGPlay.objects.filter(date__gte=self.date, date__lt=self.date+datetime.timedelta(days=1))
    