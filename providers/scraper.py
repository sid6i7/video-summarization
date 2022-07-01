from random import randint
import re
import json
from time import sleep
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


class Scraper:

    def __init__(self) -> None:
        self.transcriber = YouTubeTranscriptApi()
        self.transcriptFormatter = TextFormatter()

    def __get_video_ids_titles(self, keywords):
        """
            Scrapes video ids by querying youtube search using a bunch of keywords

            Input Parameters:
                - keywords: keywords to be used in the search

            Returns: a dictionary of video ids and titles
        """
        keywords = '+'.join(sys.argv[1:])
        response = requests.get(f'{YT_SEARCH_URL}{keywords}{YT_SEARCH_FILTER}').text
        dyn = re.search('var ytInitialData =(.*?);</script>', response)[0][20:-10]
        js = json.loads(dyn)
        videos = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        videoDetails = {}
        for video in videos:
            if 'videoRenderer' in video:
                id = video['videoRenderer']['videoId']
                title = video['videoRenderer']['title']['runs'][0]['text'].strip()
                videoDetails[id] = title

        return videoDetails
    
    def __get_transcripts(self, videoIds):
        """
            Fetches transcripts of youtube videos using video ID

            Input Parameters:
                - videoIds: list of video IDs to get a transcript of
            
            Returns: list of transcripts in text format
        """
        captions = []
        delay = randint(1, 3)
        for idx, videoId in enumerate(videoIds):
            if idx % 5 == 0 and idx != 0:
                sleep(delay)
            try:
                transcripts = self.transcriber.list_transcripts(video_id=videoId)      
                try:
                    engTranscripts = transcripts.find_transcript(['en'])
                    caption = self.transcriptFormatter.format_transcript(engTranscripts[0].fetch())
                    captions.append(caption)
                except:
                    for transcript in transcripts:
                        caption = self.transcriptFormatter.format_transcript(transcript.translate('en').fetch())
                        captions.append(caption)
                        break
            except:
                continue
            break

        return captions

    def get_video_captions(self, keywords):
        """
            Scrapes youtube by searching for keywords

            Input parameters:
                - keywords: keywords to search for or words you would put in youtube search bar
            
            Returns: a dictionary (Video Title: Video Captions)
        """
        videoDetails = self.__get_video_ids_titles(keywords=keywords)
        captions = self.__get_transcripts(videoIds=videoDetails.keys())
        
        captions = dict(zip(list(videoDetails.values()), captions))
        # or save captions somewhere??
        return captions
