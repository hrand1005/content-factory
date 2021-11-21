import argparse
import os
from strategy import strategy
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
    parser.add_argument("-c", action="store_true", 
        help="Option to edit and compile clips.")
    parser.add_argument("-u", action="store_true", 
        help="Option to upload processed video to youtube.")
    args = parser.parse_args()
    return args


# prints the number and paths of the downloaded content
def print_status(status_obj):
    print(f"\nSuccessfully yoinked {len(status_obj)} objects:")
    for status in status_obj:
        print(f"{status}")


# constructs arguments for youtube upload script, executes
def upload_to_youtube(preset):
    file_arg = f"--file {FINAL_PRODUCT}"
    priv_arg = "--privacyStatus private"
    title_arg = f"--title {preset}-prototype"
    os.system(f"python3 share/share.py {file_arg} {priv_arg} {title_arg}")


def main():
    # TODO: Find out a better way to select strategies at runtime
    args = parse_args()
    preset = args.preset.lower()

    if preset == "sekiro": 
        print(content.SEKIRO)
        query = [f"twitch api get clips -q first=3 -q game_id={content.SEKIRO}"]
        intf = strategy.TwitchStrategy("Sekiro", query) 
    else:
        print(f"Strategy '{preset}' not found. \nExiting...")
        exit(1)

    # initialize database
    database = db.ClipDatabase(preset)

    # fetch clips using strategy
    clips = intf.get_data()
    if len(clips) == 0:
        print("No new clips to fetch for {preset}.\nExiting...")
        exit(1)

    # verify that the clips don't already existin the database
    verified_clips = database.verify_clips(clips)
    if len(verified_clips) == 0:
        print("Retrieved clips already exist in the db.\nExiting...")
        exit(1)

    # download the verified clips, print the status
    # TODO: some retry-able download strategy like the folloiwng:
    # While not enough verified clips or not at max retries:
        # get next batch of clips (new query?)
        # increment retries

    dl_status = intf.download(verified_clips, RAW_DIR)
    print_status(dl_status)

    # compile step, opt in with -c
    if args.c: 
        edited_clips = compile.edit_clips(verified_clips, RAW_DIR, PROCESSED_DIR)
        compile.compile_clips(edited_clips)
    else:
        print("Exiting without compiling...")
        exit(0)

    # upload step, opt in with -u
    if args.u:
        upload_to_youtube(preset)
    else:
        print("Exiting without uploading...")
        exit(0)

    # add the clips from the uploaded vid to the database
    # TODO: decide how to handle verified clips that haven't been downlaoded
    database.insert_clips(verified_clips)

if __name__ == "__main__":
    main()
