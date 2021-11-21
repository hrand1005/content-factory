import argparse
import os
from clip import content 
from db import db
from compile import compile


RAW_DIR = "db/tmp/"
PROCESSED_DIR = "compile/tmp/"
FINAL_PRODUCT = "compiled-vid.mp4"


# parses args, ie preset
def parse_args():
    parser = argparse.ArgumentParser(
        description="Download clips, compile them into a video, and upload it to youtube.")
    parser.add_argument('--preset',
        help="Name of the preset with configurations for content regurgitation.")
    args = parser.parse_args()
    return args.preset.lower()


# prints the number and paths of the downloaded content
def print_status(status_obj):
    print(f"\nSuccessfully yoinked {len(status_obj)} objects:")
    for status in status_obj:
        print(f"{status}")


def main():
    # TODO: Find out a better way to select strategies at runtime
    preset = parse_args()
    if preset == "premiummelee":
        strategy = content.PremiumMelee()
    elif preset == "darksouls": 
        strategy = content.DarkSouls()
    elif preset == "sekiro": 
        strategy = content.Sekiro()
    else:
        print(f"Strategy '{preset}' not found. \nExiting...")
        exit(1)
    # initialize database
    database = db.ClipDatabase(preset)

    # fetch clips using strategy
    clips = strategy.fetch_clips()
    if len(clips) == 0:
        print("No new clips to fetch for PremiumMelee.\nExiting...")
        exit(1)

    # verify that the clips don't already existin the database
    verified_clips = database.verify_clips(clips)
    if len(verified_clips) == 0:
        print("Retrieved clips already exist in the db.\nExiting...")
        exit(1)

    # download the verified clips, print the status
    dl_status = content.download_clips(verified_clips, RAW_DIR)
    print_status(dl_status)

    # prompts user to manually compile -- used for testing
    print(f"\nLatest clips yoinked for {preset}!")
    compile_flag = input("Ready to edit and compile? [Y/N]\n")
    if compile_flag.lower()[0] == "y":
        edited_clips = []
        for clip in verified_clips: 
            filename = f"{clip['url'].rpartition('/')[-1]}.mp4"
            clip_path = f"{RAW_DIR}{filename}"
            # apply text overlay here, other processing should happen here
            edited_clip = compile.apply_overlay(clip, clip_path, PROCESSED_DIR)
            edited_clips.append(edited_clip)
        compile.compile_clips(edited_clips)
    else:
        print("Exiting without compiling...")
        exit(0)

    # prompts user to manually upload -- used for testing
    print(f"\nVid compiled for {preset}!")
    upload_flag = input("Ready to upload? [Y/N]\n")
    if upload_flag.lower()[0] == "y":
        file_arg = f"--file {FINAL_PRODUCT}"
        priv_arg = "--privacyStatus private"
        title_arg = f"--title {preset}-prototype"
        os.system(f"python3 share/share.py {file_arg} {priv_arg} {title_arg}")
    else:
        print("Exiting without uploading...")
        exit(0)

    # add the clips from the uploaded vid to the database
    # TODO: decide how to handle verified clips that haven't been downlaoded
    database.insert_clips(verified_clips)

if __name__ == "__main__":
    main()
