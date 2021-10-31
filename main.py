import argparse
from clip import content, clip
from db import db
from moviepy.editor import *


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download clips, compile them into a video, and upload it to youtube.")
    parser.add_argument('--preset',
        help="Name of the preset with configurations for content regurgitation.")
    args = parser.parse_args()

    return args.preset


def main():
    preset = parse_args()

    if preset == "PremiumMelee":
        strategy = content.PremiumMelee()
        database = db.ClipDatabase(preset)
    else:
        print(f"Strategy '{preset}' not found. \nExiting...")
        exit(1)

    clips = strategy.fetch_clips()
    clip_urls = clip.just_urls(clips)

    if len(clips) == 0:
        print("No new clips to fetch for PremiumMelee.\nExiting...")
        exit(1)

    verified_clip_urls = database.verify_clip_urls(clip_urls)
    
    if len(verified_clip_urls) == 0:
        print("Retrieved clips already exist in the db.\nExiting...")
        exit(1)

    # TODO: error handling might be nice, return information about how many 
    # clips were downloaded successfully
    clip.download_clips(clips, verified_clip_urls)

    database.insert_clip_urls(verified_clip_urls)

    vid_objs = []
    for filename in os.listdir('db/tmp'):
        if filename.endswith('.mp4'):
            vid_objs.append(VideoFileClip(f'db/tmp/{filename}'))

    compiled_vid = concatenate_videoclips(vid_objs)
    compiled_vid.write_videofile('compiled-vid.mp4')
    print("Vid compiled!")
    #then compile the clips randomly into a vid
    #then upload vid
    #then delete the local clips, but keep the vid
    #print url to created vid


if __name__ == "__main__":
    main()