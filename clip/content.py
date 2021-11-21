# Contains content constants and strategies, each inheriting from
# an abstract base class 'ContentCompiler'
import sys
import urllib.request
import os
import json
from abc import ABC, abstractmethod

# CREATORS
MANGO = "26551727"
DISTORTION2 = "36324138"


# GAMES

## smash
MELEE = "16282"
## 
DEMONS_SOULS_REMASTERED = "21812"
BLOODBORNE = "460636"
SEKIRO = "506415"
DS1 = "29433"
DS2 = "91423"
DS3 = "490292"

# Content Map
CONTENT_MAP = { MELEE: [MANGO] }

# Abstract class for ContentCompilers
class ContentCompiler(ABC):
    @abstractmethod
    def fetch_clips(self):
        pass

# Presets
class PremiumMelee(ContentCompiler):

    def __init__(self):
        self.name = "PremiumMelee"
        self.creators = [MANGO]
        self.queries = []

        base_query = "twitch api get clips -q first=20"
        for creator in self.creators:
            self.queries.append(f"{base_query} -q broadcaster_id={creator}")

    def fetch_clips(self):
        aggregate = self._aggregate_clips()
        return self._filter_results(aggregate)
    
    def _aggregate_clips(self):
        aggregate = []
        for query in self.queries:
            stream = os.popen(query)
            json_clips = stream.read()
            aggregate.extend(json.loads(json_clips)["data"])
        
        return aggregate
    
    def _filter_results(self, all_clips): 
        filtered_results = []
        for clip in all_clips:
            if clip["game_id"] == MELEE:
                filtered_results.append(clip)
        
        return filtered_results

class DarkSouls(ContentCompiler):

    def __init__(self):
        self.name = "DarkSouls"
        self.games = [DS1, DS2, DS3]
        self.queries = []

        base_query = "twitch api get clips -q first=4"
        for game in self.games:
            self.queries.append(f"{base_query} -q game_id={game}")

    def fetch_clips(self):
        aggregate = self._aggregate_clips()
        return self._filter_results(aggregate)
    
    def _aggregate_clips(self):
        aggregate = []
        for query in self.queries:
            stream = os.popen(query)
            json_clips = stream.read()
            aggregate.extend(json.loads(json_clips)["data"])
        
        return aggregate
    
    def _filter_results(self, all_clips): 
        return all_clips
        # filtered_results = []
        # for clip in all_clips:
        #     if clip["game_id"] == MELEE:
        #         filtered_results.append(clip)
        
        # return filtered_results

class Sekiro(ContentCompiler):

    def __init__(self):
        self.name = "Sekiro"
        self.games = [SEKIRO]
        self.queries = []

        base_query = "twitch api get clips -q first=3"
        for game in self.games:
            self.queries.append(f"{base_query} -q game_id={game}")

    def fetch_clips(self):
        aggregate = self._aggregate_clips()
        return self._filter_results(aggregate)
    
    def _aggregate_clips(self):
        aggregate = []
        for query in self.queries:
            stream = os.popen(query)
            json_clips = stream.read()
            aggregate.extend(json.loads(json_clips)["data"])
        
        return aggregate
    
    def _filter_results(self, all_clips): 
        return all_clips
        # filtered_results = []
        # for clip in all_clips:
        #     if clip["game_id"] == MELEE:
        #         filtered_results.append(clip)
        # return filtered_results
        

######### HELPER FUNCTIONS ##########

## yoinked this from some dude on github
def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

def download_clips(clips, clip_dir):
    success = []

    for i in range(len(clips)):
        clip_url = clips[i]['url']
        name = clip_url.rpartition("/")[-1]

        thumb_url = clips[i]["thumbnail_url"]
        mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"

        out_filename = name + ".mp4"
        output_path = (clip_dir + out_filename)

        try: 
            urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
            success.append(output_path)
        except: 
            print(f"Could not retrieve a clip: {mp4_url}") 

    return success


# def getToken():
#     stream = os.popen("twitch token")
#     return stream.read().split()[-1]
