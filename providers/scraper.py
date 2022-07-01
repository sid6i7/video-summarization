from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import json
import requests as rq
import sys

mod = '../'
if mod not in sys.path: sys.path.append(mod)
from config import *

arg = '+'.join(sys.argv[1:])
ini = rq.get(f'{YT_SEARCH_URL}{arg}{YT_SEARCH_FILTER}').text
dyn = re.search('var ytInitialData =(.*?);</script>', ini)[0][20:-10]
js = json.loads(dyn)
part = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

print('Downloading...')
try:
    for x in part:
        try:
            id_ = x['videoRenderer']['videoId']
            txt = yta.get_transcript(id_)
            with open(f'{CC_DIR}{id_}', 'w') as f:
                print(f'Working with {id_}')
                for i in txt: f.write(f'{i["text"]} ')
                f.write('\n')
        except: continue
except: None

print('---END---')
