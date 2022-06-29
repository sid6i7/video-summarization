import re
import json
import requests as rq
import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import *

arg = '+'.join(sys.argv[1:])
ini = rq.get(f'{YT_SEARCH_URL}{arg}{YT_SEARCH_FILTER}').text
dyn = re.search('var ytInitialData =(.*?);</script>', ini)[0][20:-10]
js = json.loads(dyn)
videos = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

print('Downloading...')
try:
    for video in videos:
        print(video['videoRenderer']['videoId'])
        os.system(f'youtube-dl -x --audio-format wav https://www.youtube.com/watch?v={video["videoRenderer"]["videoId"]} -o {AUDIO_DIR}/{video["videoRenderer"]["videoId"]}.wav')
except: None
