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
        description="Download content, compile them into a video, and upload it to youtube.")
    parser.add_argument('--preset',
        help="Name of the preset with configurations for content regurgitation.")
    parser.add_argument("-c", action="store_true", 
        help="Option to edit and compile content.")
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
    database = db.ContentDatabase(preset)

    # fetch content using strategy
    content_objs = intf.get_content()
    if len(content_objs) == 0:
        print("No new content to fetch for {preset}.\nExiting...")
        exit(1)

    # verify that the content don't already existin the database
    verified_content = database.verify_content(content_objs)
    if len(verified_content) == 0:
        print("Retrieved content already exist in the db.\nExiting...")
        exit(1)

    # download the verified content, print the status
    # TODO: some retry-able download strategy like the folloiwng:
    # While not enough verified content or not at max retries:
        # get next batch of content (new query?)
        # increment retries

    dl_status = intf.download(verified_content, RAW_DIR)
    print_status(dl_status)

    # compile step, opt in with -c
    if args.c: 
        edited_content = compile.edit_content(verified_content, RAW_DIR, PROCESSED_DIR)
        compile.compile_content(edited_content)
    else:
        print("Exiting without compiling...")
        exit(0)

    # upload step, opt in with -u
    if args.u:
        upload_to_youtube(preset)
    else:
        print("Exiting without uploading...")
        exit(0)

    # add the content from the uploaded vid to the database
    # TODO: decide how to handle verified content that haven't been downlaoded
    database.insert_content(verified_content)

if __name__ == "__main__":
    main()
