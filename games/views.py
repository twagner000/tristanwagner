from django.shortcuts import render
import requests
import xml.etree.ElementTree as ET
import datetime
from django.conf import settings

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
        g['numplays'] = item.find('numplays').text

    return render(request, 'games/index.html', {'plays':plays, 'favs':favs, 'bgg_user':settings.BGG_USER})