import os
import sys
import json
import content

# QUERY_PARAMS = { "braodcaster_id": None, 
#                  "game_id": None, 
#                  "id": None,
#                  "after": None,
#                  "before": None,
#                  "ended_at": None,
#                  "first": None,
#                  "started_at": None }

# def getToken():
#     stream = os.popen("twitch token")
#     return stream.read().split()[-1]

def parseArgs():
    if len(sys.argv) != 2:
        print("Usage: contentFactory.py <preset_name>")
        exit(1)
    
    if (sys.argv[1].lower()) == "premiummelee":
        return content.PremiumMelee

    print(f"{sys.argv[1]} not recognized, exiting...")
    exit(1)

def buildQueryParams(query_params):
    query_string = ""
    for key in query_params:
        if query_params[key]:
            query_string += f"-q {key}={query_params[key]}"
    
    #print(f"Query String: {query_string}")
    return query_string

def getClips(category, query_string):
    clips = {}
    for creator in content.CONTENT_MAP[category]:
        query_string += f" -q broadcaster_id={creator}"
        full_command = f"twitch api get clips {query_string}"
        #print(f"Full Command: {full_command}")
        
        stream = os.popen(full_command)
        json_clips = stream.read()
        creator_clips = []
        for clip in json.loads(json_clips)["data"]:
            creator_clips.append(clip)
            clips[clip["broadcaster_name"]] = creator_clips
    
    return clips

def filterClips(clips, filter):
    if filter != None:
        print("Not yet implemented")
    
    return clips

def main():
    #token = getToken()
    preset = parseArgs()
    query_string = buildQueryParams(preset.query_params)
    clips = getClips(preset.category, query_string)
    filtered_results = filterClips(clips, preset.filter)
    #print(f"Here's the filtered results: {filtered_results}")
    # for clip in clips:
    #     print("Here's a clip: %s", clips)
    clip_urls = []
    for creator in filtered_results:
        for clip in filtered_results[creator]:
            clip_urls.append(clip['url'])
    
    print(f"Here are the clip urls: {clip_urls}")

if __name__ == "__main__":
    main()