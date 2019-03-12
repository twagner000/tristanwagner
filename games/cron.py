from django_cron import CronJobBase, Schedule
import datetime

from . import models
from django.conf import settings
import requests
import xml.etree.ElementTree as ET

class RecentBGGPlaysCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=60)
    code = 'games.recent_bgg_plays'
    
    def do(self):
        xml = requests.get("https://boardgamegeek.com/xmlapi2/plays", params={
            'username':settings.BGG_USER,
            'mindate':(datetime.date.today() - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
            })
        root = ET.fromstring(xml.text.encode('utf8'))
        for p in root.iter('play'):
            play = models.BGGPlay(bgg_play_id=int(p.attrib['id']))
            item = p.find('item')
            play.bgg_game_id = item.attrib['objectid']
            play.game_name = item.attrib['name']
            play.date = datetime.datetime.strptime(p.attrib['date'], '%Y-%m-%d').date()
            play.quantity = int(p.attrib['quantity'])
            play.save()
        
        