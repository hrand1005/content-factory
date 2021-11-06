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

    return args.preset.lower()


def main():
    preset = parse_args()

    # TODO: Find out a better way to select strategies at runtime
    if preset == "premiummelee":
        strategy = content.PremiumMelee()
    elif preset == "darksouls": 
        strategy = content.DarkSouls()
    elif preset == "sekiro": 
        strategy = content.Sekiro()
    else:
        print(f"Strategy '{preset}' not found. \nExiting...")
        exit(1)

    database = db.ClipDatabase(preset)

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

    # linux terminal commands to compile method
    # if we go with this, remember to add it ot a requirements.txt
    # NOTE: Works, but produces some errors in the video output. 
    with open('clips.txt', 'w') as f:    
        for filename in os.listdir('db/tmp'):
            if filename.endswith('.mp4'):
                f.write(f"file 'db/tmp/{filename}\n")

    # TODO: This method of compiling vids is quite slow. Optimize? Use .sh?
    # vid_objs = []
    # for filename in os.listdir('db/tmp'):
    #     if filename.endswith('.mp4'):
    #         vid_objs.append(VideoFileClip(f'db/tmp/{filename}'))

    # compiled_vid = concatenate_videoclips(vid_objs, method='compose')
    # compiled_vid.write_videofile('compiled-vid.mp4')
    # print("Vid compiled!")

    #then compile the clips randomly into a vid
    #then upload vid
    #then delete the local clips, but keep the vid
    #print url to created vid


if __name__ == "__main__":
    main()