from django.shortcuts import render, redirect
import requests
import xml.etree.ElementTree as ET
import datetime
from django.conf import settings

from django.contrib.admin.views.decorators import staff_member_required
import re
from .models import BGGUserSearch, BGGGame, BGGUserRating, BGGUser
from . import models
import time

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import defaultdict
from . import serializers



def usersearch(q,page=1):
    r = requests.get("http://boardgamegeek.com/geeksearch.php", params={
        'action':'search',
        'objecttype':'user',
        'q':q,
        'pageID':page})
    if r.status_code != 200:
        raise Exception('no code 200')
    return r.text
    
def userratings(username,repeat=False):
    r = requests.get("http://www.boardgamegeek.com/xmlapi2/collection", params={
        'username':username,
        'excludesubtype':'boardgameexpansion',
        'minrating':1,
        'stats':1})
    if r.status_code == 200:
        return r.text
    else:
        if repeat:
            raise Exception('no code 200')
        else:
            time.sleep(5)
            return userratings(username,repeat=True)

@staff_member_required
def findbggusers(request):
    #portions of this code are credit to https://github.com/JStech/bggrec
    q = request.GET['q']
    n_re = re.compile(r'Search Results \(([0-9]+) Matches?\)')
    user_re = re.compile(r"data-urlusername='([^']+)'")
    users = []
    
    html = usersearch(q)
    n_results = n_re.search(html)
    n = int(n_results.group(1)) if n_results else 0
    for page in range(1, min(11,(n+99)//100 + 1)):
        if page>1:
            html = usersearch(q,page)
        user_results = user_re.findall(html)
        if not user_results:
            break
        users += user_results
    us = BGGUserSearch(q=q, users=','.join(users))
    us.save()
    
    return render(request, 'games/findbggusers.html', {'search':us})
    
@staff_member_required
def userstoquery(request):
    users = []
    for us in BGGUserSearch.objects.all():
        users += us.user_list()
    users = set(users)
    #http://www.boardgamegeek.com/xmlapi2/collection?username=twagner&excludesubtype=boardgameexpansion&minrating=1&stats=1
    return render(request, 'games/userstoquery.html', {'users':users})
    
@staff_member_required
def getuserratings(request):
    username = request.GET['username']
    xml = userratings(username)
    root = ET.fromstring(xml.encode('utf8'))
    
    user = BGGUser.objects.filter(user=username.lower())
    if not user:
        user = BGGUser(user=username.lower())
        user.save()
    else:
        user = user[0]
    
    for i in root.iter('item'):
        if i.attrib['subtype'] != 'boardgame':
            continue
        objectid = int(i.attrib['objectid'])
        game = BGGGame.objects.filter(objectid=objectid)
        if not game:
            game_name = i.find('name').text
            yearpublished = i.find('yearpublished')
            s = i.find('stats')
            game = BGGGame(
                objectid=objectid,
                name=game_name,
                yearpublished=int(yearpublished.text) if yearpublished else None,
                minplayers=s.attrib.get('minplayers',None),
                maxplayers=s.attrib.get('maxplayers',None),
                minplaytime=s.attrib.get('minplaytime',None),
                maxplaytime=s.attrib.get('maxplaytime',None),
                playingtime=s.attrib.get('playingtime',None),
                numowned=s.attrib.get('numowned',None)
                )
            game.save()
        else:
            game = game[0]
        rating = float(i.find('stats').find('rating').attrib['value'])
        numplays = int(i.find('numplays').text)
        rating = user.bgguserrating_set.create(
            game=game,
            rating=rating,
            numplays=numplays
            )
    
    ratings = BGGUserRating.objects.filter(user=user)
        
    return render(request, 'games/getuserratings.html', {'user':user, 'ratings':ratings})
    
class PlayDateList(generics.ListAPIView):
    queryset = models.BGGPlayDate.objects.filter(date__gte=datetime.date(datetime.date.today().year,1,1), date__lte=datetime.date.today())
    serializer_class = serializers.PlayDateSerializer
    permission_classes = tuple()
    
class PlayList(generics.ListAPIView):
    queryset = models.BGGPlay.objects.filter(date__gte=datetime.date(datetime.date.today().year,1,1), date__lte=datetime.date.today())
    serializer_class = serializers.PlaySerializer
    permission_classes = tuple()
    
class Past52WeeksList(APIView):
    permission_classes = tuple()

    def get(self, request, format=None):
        weeks = []
        cur_week_start = datetime.date.today()
        cur_week_start -= datetime.timedelta(days=cur_week_start.weekday())
        cur_week_start -= datetime.timedelta(days=52*7)
        for i in range(52):
            next_week_start = cur_week_start + datetime.timedelta(days=7)
            weeks.append({'week':cur_week_start, 'count':models.BGGPlay.objects.filter(date__gte=cur_week_start, date__lt=next_week_start).count()})
            cur_week_start = next_week_start
        return Response(weeks)
        
def populate_play_dates(request):
    models.BGGPlayDate.objects.all().delete()
    curdate = datetime.date(datetime.date.today().year-5,1,1)
    enddate = datetime.date(curdate.year+30,1,1)
    bulk_dates = []
    while curdate < enddate:
        bulk_dates.append(models.BGGPlayDate(date=curdate))
        curdate += datetime.timedelta(days=1)
    models.BGGPlayDate.objects.bulk_create(bulk_dates)
    return redirect('games:index')
    
def index(request):
    #recent plays data
    xml = requests.get("https://boardgamegeek.com/xmlapi2/plays", params={
        'username':settings.BGG_USER,
        'mindate':(datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        })
    root = ET.fromstring(xml.text.encode('utf8'))
    plays = []
    for p in root.iter('play'):
        play = {}
        item = p.find('item')
        play['date'] = datetime.datetime.strptime(p.attrib['date'], '%Y-%m-%d').date()
        play['quantity'] = int(p.attrib['quantity'])
        play['name'] = item.attrib['name']
        play['game_id'] = item.attrib['objectid']
        play['expansions'] = []
        for s in item.find('subtypes').iter('subtype'):
            if s.attrib['value'] == 'boardgameexpansion':
                play['expansion_yes'] = True
                break
        plays.append(play)
    for p in plays:
        if 'expansion_yes' in p:
            b,sep,e = p['name'].partition(':')
            for p2 in plays:
                if p2['name'] == b.strip() and p2['date'] == p['date']:
                    p2['expansions'].append({'name':e.strip(), 'game_id':p['game_id']})
                    plays = [p3 for p3 in plays if p3['name'] != p['name']]
                    break
        
    #top 10 data
    favs = []
    xml = requests.get("https://boardgamegeek.com/xmlapi2/user", params={'name':settings.BGG_USER, 'top':1})
    root = ET.fromstring(xml.text.encode('utf8'))
    top = root.find('top')
    if top:
        for item in top.iter('item'):
            favs.append({'id': item.attrib['id']})
    xml = requests.get("https://boardgamegeek.com/xmlapi2/thing", params={'id':','.join(g['id'] for g in favs)})
    root = ET.fromstring(xml.text.encode('utf8'))
    for g in favs:
        item = root.find("item[@id='%s']" % g['id'])
        g['name'] = item.find("name[@type='primary']").attrib['value']
        g['thumbnail'] = item.find('thumbnail').text
        g['description'] = item.find('description').text
        g['minplayers'] = item.find('minplayers').attrib['value']
        g['maxplayers'] = item.find('maxplayers').attrib['value']
        g['minplaytime'] = item.find('minplaytime').attrib['value']
        g['maxplaytime'] = item.find('maxplaytime').attrib['value']
    xml = requests.get("https://boardgamegeek.com/xmlapi2/collection", params={'username':settings.BGG_USER, 'id':','.join(g['id'] for g in favs)})
    root = ET.fromstring(xml.text.encode('utf8'))
    for g in favs:
        item = root.find("item[@objectid='%s']" % g['id'])
        g['numplays'] = item.find('numplays').text if item else ''
        
    #weekly plays
    weeks = []
    cur_week_start = datetime.date.today()
    cur_week_start -= datetime.timedelta(days=cur_week_start.weekday())
    cur_week_start -= datetime.timedelta(days=52*7)
    for i in range(52):
        next_week_start = cur_week_start + datetime.timedelta(days=7)
        weeks.append({'week':cur_week_start, 'count':models.BGGPlay.objects.filter(date__gte=cur_week_start, date__lt=next_week_start).count()})
        cur_week_start = next_week_start
        
    

    return render(request, 'games/index.html', {'plays':plays, 'favs':favs, 'bgg_user':settings.BGG_USER, 'weeks': weeks, 'weeks_sum':sum(v['count'] for v in weeks)})