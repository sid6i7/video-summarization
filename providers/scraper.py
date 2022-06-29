import re
import json
import requests
import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import *
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

srt = YouTubeTranscriptApi.get_transcript("7W3oxSkq_rQ")

text = TextFormatter().format_transcript(srt)
print(text.replace('\n', " "))

class Scraper:

    def __init__(self) -> None:
        self.transcriber = YouTubeTranscriptApi()
        self.transcriptFormatter = TextFormatter()

    def get_video_ids(self, keywords):
        """
            Scrapes video ids by querying youtube search using a bunch of keywords

            Input Parameters:
                - keywords: keywords to be used in the search

            Returns: video ids
        """
        keywords = '+'.join(keywords)
        response = requests.get(f'{YT_SEARCH_URL}{keywords}{YT_SEARCH_FILTER}').text
        dyn = re.search('var ytInitialData =(.*?);</script>', response)[0][20:-10]
        js = json.loads(dyn)
        videos = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        videoIds = []
        for video in videos:
            if ['videoRenderer']['videoId'] in video:
                videoIds.append(video['videoRenderer']['videoId'])

        return videoIds
    
    def get_transcripts(self, videoIds):
        """
            Fetches transcripts of youtube videos using video ID

            Input Parameters:
                - videoIds: list of video IDs to get a transcript of
            
            Returns: list of transcripts in text format
        """
        rawTranscripts = self.transcriber.get_transcripts(video_ids=videoIds)
        transcripts = [transcript.replace("\n", " ") for transcript in self.transcriptFormatter.format_transcripts(rawTranscripts)]

        return transcripts
