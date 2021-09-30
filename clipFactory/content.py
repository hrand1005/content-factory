import os
import json
from abc import ABC, abstractmethod
#import datetime

# Creators
MANGO = "26551727"

# Games
MELEE = "16282"

# Content Map
CONTENT_MAP = { MELEE: [MANGO] }

# Abstract class for ContentCompilers
class ContentCompiler(ABC):
    @abstractmethod
    def fetchClips(self):
        pass

# Presets
class PremiumMelee(ContentCompiler):
    def __init__(self):
        self.creators = [MANGO]
        self.queries = []

        base_query = "twitch api get clips -q first=10"
        for creator in self.creators:
            self.queries.append(f"{base_query} -q broadcaster_id={creator}")

    def fetchClips(self):
        aggregate = self._aggregateClips()
        return self._filterResults(aggregate)
    
    def _aggregateClips(self):
        aggregate = []
        for query in self.queries:
            stream = os.popen(query)
            json_clips = stream.read()
            aggregate.extend(json.loads(json_clips)["data"])
        
        return aggregate
    
    def _filterResults(self, all_clips): 
        filtered_results = []
        for clip in all_clips:
            if clip["game_id"] == MELEE:
                filtered_results.append(clip)
        
        return filtered_results
