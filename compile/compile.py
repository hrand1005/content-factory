import os
import cv2

COMPILE_COMMAND = "echo not implemented" 

# def apply_overlay(clip_path):
    #construct overlay
    #apply overlay 
        #--> perhaps we can also compress in this step to save time? 
    #report done or return
    #print("apply_overlay() not yet implemented")

def compile_clips(): # take a clips or strategy parameter
    # compile the given clips. Maybe this should involve a strategy? 
    # for example, the strategy could determine the order of clips, the length
    # of the entire video, what clips to include / exclude
    os.system(COMPILE_COMMAND)

def apply_overlay(clip_data): # also provide strategy?
    # get clip path
    clip_url = clip_data["url"]
    name = clip_url.rpartition("/")[-1] + ".mp4"
    clip_path = "./db/tmp/" + name #use clip data to construct path
    print(f"Clip Path: {clip_path}")
    print(f"Verifying path: {os.path.exists(clip_path)}")
    cap = cv2.VideoCapture(clip_path)

    # define an overlay
    overlay = f"{clip_data['broadcaster_name']}\n{clip_data['title']}"
    frame_number = 0
    while(True):
        print(f"Chugging along at frame: {frame_number}")
        frame_number += 1
        # Capture frames in the video
        ret, frame = cap.read()
    
        #TODO: get this from the strategy
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(frame, overlay, (50, 50), font, 1, (255, 255, 255),
                2, cv2.LINE_4)

        #TODO: remove this?
        cv2.imshow('video', frame)

        #TODO: remove
        # creating 'q' as the quit for the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the cap object
    cap.release()
    #close all windows
    cv2.destroyAllWindows()
             


