import os
import sys
import requests
import urllib.request
from db.db import ClipDatabase

def insert_clips(strategy, clip_urls):
    db = ClipDatabase(strategy)
    db.insert_clips(clip_urls)

def verified_unique(strategy, clip_urls):
    db = ClipDatabase(strategy)
    return db.verify_clips(clip_urls)

# yoinked this from some dude on github
def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()

def download_clips(clips, clip_urls):

    client_id = '2wz5uou0dswzpv17opht3tbr73j9rf'
    basepath = 'db/tmp/'

    for i in range(len(clips)):
        slug = clip_urls[i].rpartition('/')[-1]

        print(clips[i])
        thumb_url = clips[i]['thumbnail_url']
        mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"
        out_filename = slug + ".mp4"
        output_path = (basepath + out_filename)
        #clip_info = requests.get("https://api.twitch.tv/kraken/clips/" + slug, headers={"Client-ID": client_id, "Accept":"application/vnd.twitchtv.v6+json"}).json()
        urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
        #print(f"Could not download clip from url: {url}")