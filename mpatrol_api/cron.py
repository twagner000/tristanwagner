from django.db.models import Sum
from django_cron import CronJobBase, Schedule
import datetime
import json

from . import models
from . import constants

class StructureInterestCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=60)
    code = 'mpatrol_api.structure_interest'
    
    def do(self):
        today = datetime.datetime.now().astimezone(constants.pacific).date()
        for game in models.Game.objects.filter(ended_date__isnull=True).exclude(last_interest_date__gte=today):
            players = game.player_set.annotate(interest_gold=Sum('structures__interest_gold'), interest_xp=Sum('structures__interest_xp'))
            for p in players.filter(interest_gold__gt=0) | players.filter(interest_xp__gt=0):
                interest_gold_amt = int(p.gold*p.interest_gold/100)
                interest_xp_amt = int(p.xp*p.interest_xp/100)
                p.gold += interest_gold_amt
                p.xp += interest_xp_amt
                msg = 'You earned {0} gold and {1} xp interest from your structures.'.format(interest_gold_amt, interest_xp_amt)
                json_data = {'work_gold':interest_gold_amt, 'work_xp':interest_xp_amt}
                log = models.PlayerLog(player=p, action='interest', description=msg, json_data=json.dumps(json_data))
                p.save()
                log.save()
            game.last_interest_date = datetime.datetime.now()
            game.save()