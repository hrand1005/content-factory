import argparse, os, yaml
from strategy import strategy
from db import db
from compile import compile


RAW_DIR = "db/tmp/"
PROCESSED_DIR = "compile/tmp/"
FINAL_PRODUCT = "compiled-vid.mp4"


# parses args, ie preset
def parse_args():
    parser = argparse.ArgumentParser(
        description="Download content, compile them into a video, and upload it to youtube.")
    parser.add_argument("--file",
        help="Name of yaml file with configurations for content regurgitation.")
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
def upload_to_youtube(name):
    file_arg = f"--file {FINAL_PRODUCT}"
    priv_arg = "--privacyStatus private"
    title_arg = f"--title {name}-prototype"
    os.system(f"python3 share/share.py {file_arg} {priv_arg} {title_arg}")


def main():
    args = parse_args()
    # load context from file
    with open(args.file, "r") as f:
        context = yaml.safe_load(f)

    # use context to initialize strategy and database
    concrete_strategy = strategy.select_strategy(context["source"], context["params"])
    database = db.ContentDatabase(context["name"])

    # fetch content using strategy
    content_objs = concrete_strategy.get_content()
    if len(content_objs) == 0:
        print("No new content to fetch for {context['name']}.\nExiting...")
        exit(1)

    # verify that the content don't already existin the database
    verified_content = database.verify_content(content_objs)
    if len(verified_content) == 0:
        print("Retrieved content already exist in the db.\nExiting...")
        exit(1)

    # download content, print status TODO: retry downloading if fails?
    fetched_content = concrete_strategy.download(verified_content, RAW_DIR)
    print_status(fetched_content)

    # compile step, opt in with -c
    if args.c: 
        edited_content = compile.edit_content(fetched_content, RAW_DIR, PROCESSED_DIR)
        compile.compile_content(edited_content)
    else:
        print("Exiting without compiling...")
        exit(0)

    # upload step, opt in with -u
    if args.u:
        upload_to_youtube(context["name"])
    else:
        print("Exiting without uploading...")
        exit(0)

    # add the content from the uploaded vid to the database
    # TODO: decide how to handle verified content that haven't been downlaoded
    database.insert_content(fetched_content)

if __name__ == "__main__":
    main()
