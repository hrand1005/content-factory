# Contains content constants and strategies, each inheriting from
# an abstract base class 'ContentCompiler'

import os
import json
from abc import ABC, abstractmethod

# Creators
MANGO = "26551727"

# Games
MELEE = "16282"

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
