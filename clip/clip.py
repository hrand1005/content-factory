# This library contains tools to manage clips -- get their urls, download them, etc.

import sys
import urllib.request

# def getToken():
#     stream = os.popen("twitch token")
#     return stream.read().split()[-1]

def just_urls(clip_dicts):
    urls = []
    for clip in clip_dicts:
        urls.append(clip["url"])
    
    return urls

# yoinked this from some dude on github
def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

# TODO: Some error handling might be nice
def download_clips(clips, clip_urls):
    basepath = 'db/tmp/'

    for i in range(len(clips)):
        slug = clip_urls[i].rpartition('/')[-1]

        thumb_url = clips[i]['thumbnail_url']
        mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"
        out_filename = slug + ".mp4"
        output_path = (basepath + out_filename)
        urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
