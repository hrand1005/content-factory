import os
import sys
import urllib.request
import clip.content as content

# def getToken():
#     stream = os.popen("twitch token")
#     return stream.read().split()[-1]

def parse_args(preset):
    # if len(sys.argv) != 2:
    #     print("Usage: contentFactory.py <preset_name>")
    #     exit(1)
    
    # if (sys.argv[1].lower()) == "premiummelee":
    #     return content.PremiumMelee()

    if preset.lower() == "premiummelee":
        return content.PremiumMelee()

    print(f"{sys.argv[1]} not recognized, exiting...")
    exit(1)

def just_urls(clip_dicts):
    urls = []
    for clip in clip_dicts:
        urls.append(clip["url"])
    
    return urls

def get_clips(preset):
    #token = getToken()
    strategy = parse_args(preset)
    clip_dicts = strategy.fetch_clips()
    #print(f"Here are the clip dicts: {clip_dicts}\n")

    return just_urls(clip_dicts)
    #print(f"And here are just the urls: {clip_urls}\n")

def get_clips_with_info(preset):
    strategy = parse_args(preset)
    return strategy.fetch_clips()
    #print(f"Here are the clip dicts: {clip_dicts}\n")

    #print(f"And here are just the urls: {clip_urls}\n")

