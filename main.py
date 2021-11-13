import argparse
from clip import content 
from db import db


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download clips, compile them into a video, and upload it to youtube.")
    parser.add_argument('--preset',
        help="Name of the preset with configurations for content regurgitation.")
    args = parser.parse_args()

    return args.preset.lower()

def print_status(status_obj):
    print(f"\nSuccessfully yoinked {len(status_obj)} objects:")
    for status in status_obj:
        print(f"{status}")

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
    clip_urls = content.just_urls(clips)

    if len(clips) == 0:
        print("No new clips to fetch for PremiumMelee.\nExiting...")
        exit(1)

    verified_clip_urls = database.verify_clip_urls(clip_urls)
    
    if len(verified_clip_urls) == 0:
        print("Retrieved clips already exist in the db.\nExiting...")
        exit(1)

    # TODO: error handling might be nice, return information about how many 
    # clips were downloaded successfully
    dl_status = content.download_clips(clips)
    print_status(dl_status)

    # TODO: is this the right place to do this? --> may want to move to after publishing step
    database.insert_clip_urls(verified_clip_urls)

    # TODO: further vid editing before encoding and compilation step 

    print(f"\nLatest clips yoinked for {preset}! To compile, run ./compile_clips.sh")

    #then upload vid
    #then delete the local clips, but keep the vid

if __name__ == "__main__":
    main()
