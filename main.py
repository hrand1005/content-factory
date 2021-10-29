from clip import content, clip
from db import db_util


def main():

    #TODO: Determine strategy here at runtime
    if True:
        strategy = content.PremiumMelee()
    else:
        print("Strategy '' not found. \nExiting...")
        exit(1)

    clips = strategy.fetch_clips()
    clip_urls = clip.just_urls(clips)

    if len(clips) == 0:
        print("No new clips to fetch for PremiumMelee.\nExiting...")
        exit(1)

    # get db connection
    verified_clips = db_util.verified_unique("PremiumMelee", clip_urls)
    
    if len(verified_clips) == 0:
        print("Retrieved clips already exist in the db.\nExiting...")
        exit(1)

    db_util.download_clips(clips, verified_clips)

    db_util.insert_clips("PremiumMelee", verified_clips)

    #check if clips are in db 
    #verified_clips = db.verifiedUnique(db_conn, table, clips)

    #then download the URLs

    #then compile the clips randomly into a vid
    #then upload vid
    #then add clips to database
    #then delete the local clips, but keep the vid
    #print url to created vid
    #print(verified_clips)


if __name__ == "__main__":
    main()