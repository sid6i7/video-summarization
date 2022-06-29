import re
import json
import requests as rq
import sys
import os

arg = '+'.join(sys.argv[1:])
ini = rq.get(f'https://www.youtube.com/results?search_query={arg}&sp=EgIYAQ%253D%253D').text
dyn = re.search('var ytInitialData =(.*?);</script>', ini)[0][20:-10]
js = json.loads(dyn)
part = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

print('Downloading...')
try:
    for x in part:
        print(x['videoRenderer']['videoId'])
        os.system(f'youtube-dl -x --audio-format wav https://www.youtube.com/watch?v={x["videoRenderer"]["videoId"]} -o yt-aud/{x["videoRenderer"]["videoId"]}.wav')
except: None
