import os
import sys
import json
import urllib.request
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def get_content():
        pass

    @abstractmethod
    def download():
        pass

class TwitchStrategy(Strategy):
    def __init__(self, name, queries): #TODO:maybe add creators and games params?
        self.name = name 
        self.queries = queries

    def get_content(self):
        clips = self._aggregate_clips()
        if len(clips) == 0:
            print("No clips found for this strategy.")
            return
        return clips
    
    def download(self, clips, out_dir):
        success = []
        for clip in clips:
            mp4_url = self._get_mp4_url(clip)
            out_path = self._get_out_path(clip, out_dir)
            #try: 
            urllib.request.urlretrieve(mp4_url, out_path, reporthook=self._dl_progress)
            success.append(out_path)
            #except: 
                #print(f"Could not retrieve a clip: {mp4_url}") 
        return success

    def _get_out_path(self, clip, out_dir):
        name = clip["url"].rpartition("/")[-1]
        filename = name + ".mp4"
        return out_dir + filename

    def _get_mp4_url(self, clip):
        thumb_url = clip["thumbnail_url"]
        return thumb_url.split("-preview",1)[0] + ".mp4"

    def _aggregate_clips(self):
        aggregate = []
        for query in self.queries:
            stream = os.popen(query)
            json_clips = stream.read()
            aggregate.extend(json.loads(json_clips)["data"])
        return aggregate

    def _dl_progress(self, count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write("\r...%d%%" % percent)
        sys.stdout.flush()
