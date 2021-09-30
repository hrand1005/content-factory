import os
import sys
import json
import content

# def getToken():
#     stream = os.popen("twitch token")
#     return stream.read().split()[-1]

def parseArgs():
    if len(sys.argv) != 2:
        print("Usage: contentFactory.py <preset_name>")
        exit(1)
    
    if (sys.argv[1].lower()) == "premiummelee":
        return content.PremiumMelee()

    print(f"{sys.argv[1]} not recognized, exiting...")
    exit(1)

def justUrls(clip_dicts):
    urls = []
    for clip in clip_dicts:
        urls.append(clip["url"])
    
    return urls

def main():
    #token = getToken()
    preset = parseArgs()
    clip_dicts = preset.fetchClips()
    print(f"Here are the clip dicts: {clip_dicts}\n")

    clip_urls = justUrls(clip_dicts)
    print(f"And here are just the urls: {clip_urls}\n")

if __name__ == "__main__":
    main()