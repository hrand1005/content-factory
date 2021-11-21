import os


def apply_overlay(clip_obj, clip_path, output_dir):
    #construct overlay
    #ffmpeg -i $file -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf:text='TEXT':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=0:y=0" -codec:a copy $file
    overlay_text = f"{clip_obj['broadcaster_name']}\n{clip_obj['title']}"
    overlay = f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf:text='{overlay_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=0:y=0"
    #apply overlay 
        #--> perhaps we can also compress in this step to save time? 
    #report done or return
    output_file = f"{output_dir}{clip_obj['title'].replace(' ', '')}.mp4"
    os.system(f"ffmpeg -i {clip_path} -vf {overlay} -codec:a copy {output_file}")
    return output_file

def compile_clips(clip_paths): # take a clips or strategy parameter
    # compile the given clips. Maybe this should involve a strategy? 
    # for example, the strategy could determine the order of clips, the length
    # of the entire video, what clips to include / exclude
    for clip in clip_paths:
        basename = clip.strip(".mp4")
        os.system(f"ffmpeg -i {clip} -c:v libx264 -preset slow -crf 22 -c:a copy {basename}.mkv")
        echo = f"echo \"file '{basename}.mkv'\" >> clips.txt"
        os.system(echo)

    os.system("ffmpeg -f concat -safe 0 -i clips.txt compiled-vid.mp4")

# for now, just applies an overlay to all the clips
def edit_clips(clips, input_dir, output_dir):
    edited_clips = []
    for clip in clips: 
        filename = f"{clip['url'].rpartition('/')[-1]}.mp4"
        clip_path = f"{input_dir}{filename}"
        # apply text overlay here, other processing should happen here
        edited_clip = apply_overlay(clip, clip_path, output_dir)
        edited_clips.append(edited_clip)

    return edited_clips
