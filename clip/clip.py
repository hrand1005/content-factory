# This library contains tools to manage clips -- get their urls, download them, etc.

# def getToken():
#     stream = os.popen("twitch token")
#     return stream.read().split()[-1]

def just_urls(clip_dicts):
    urls = []
    for clip in clip_dicts:
        urls.append(clip["url"])
    
    return urls
