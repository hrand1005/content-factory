from clip import clip_util
from db import db_util

def main():
    clips = clip_util.get_clips("PremiumMelee")

    if len(clips) == 0:
        print("No new clips to fetch for PremiumMelee.\nExiting...")
        exit(0)

    # get db connection
    verified_clips = db_util.verified_unique("PremiumMelee", clips)
    
    #db_util.insert_clips(db_conn, table, clips)
    #check if clips are in db 
    #verified_clips = db.verifiedUnique(db_conn, table, clips)

    #then download the URLs

    #then compile the clips randomly into a vid
    #then upload vid
    #then add clips to database
    #then delete the local clips, but keep the vid
    #print url to created vid
    print(clips)



if __name__ == "__main__":
    main()