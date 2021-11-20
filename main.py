import argparse
import os
from clip import content 
from db import db
from compile import compile

CLIP_DIR = "./db/tmp/"

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

    if len(clips) == 0:
        print("No new clips to fetch for PremiumMelee.\nExiting...")
        exit(1)

    verified_clips = database.verify_clips(clips)
    print(f"Found {len(verified_clips)} verified clips, tryna yoink.")
    
    if len(verified_clips) == 0:
        print("Retrieved clips already exist in the db.\nExiting...")
        exit(1)

    dl_status = content.download_clips(verified_clips, CLIP_DIR)
    print_status(dl_status)

    # TODO: is this the right place to do this? --> may want to move to after publishing step
    database.insert_clips(verified_clips)

    # prompts user to manually compile -- used for testing
    print(f"\nLatest clips yoinked for {preset}!")
    compile_flag = input("Ready to edit and compile? [Y/N]\n")

    if compile_flag.lower()[0] == "y":
        edited_clips = []
        print("applying overlays...")
        for clip in verified_clips: 
            out_dir = "compile/tmp/"
            # TODO: unify this logic somewhere. Maybe a class for a clip object so
            # we can have one thing to refer to? think: verified flags, name,
            # filename, preprocessed path, postprocessed path, etc.
            clip_url = clip['url']
            filename = f"{clip_url.rpartition('/')[-1]}.mp4"

            clip_path = f"{CLIP_DIR}{filename}"
            edited_clip = compile.apply_overlay(clip, clip_path, out_dir)
            edited_clips.append(edited_clip)

        print("compiling...")
        print(f"compiling these clips: {edited_clips}")
        compile.compile_clips(edited_clips)
        # os.system("./compile_clips.sh")
    else:
        print("Exiting without compiling...")
        exit(0)

    #then upload vid
    #then delete the local clips, but keep the vid

    # prompts user to manually upload -- used for testing
    print(f"\nVid compiled for {preset}!")
    upload_flag = input("Ready to upload? [Y/N]\n")

    if upload_flag.lower()[0] == "y":
        print("Uploading...")
        cmd = f"python3 share/share.py --file compiled-vid.mp4 --privacyStatus private --title {preset}-prototype"
        os.system(cmd)
    else:
        print("Exiting without uploading...")
        exit(0)

if __name__ == "__main__":
    main()
