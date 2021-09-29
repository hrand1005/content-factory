from enum import Enum
#import datetime

# Creators
MANGO = "26551727"

# Games
MELEE = "16282"

# Content Map
CONTENT_MAP = { MELEE: [MANGO] }

# Presets
class PremiumMelee():
    category = MELEE
    filter = {"game_id": MELEE}
    query_params = { "first": 2 } 
                     #"started_at": datetime.datetime.now(datetime.timzeone.utc.isoformat()) }
    