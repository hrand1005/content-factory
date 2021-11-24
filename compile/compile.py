import os


def apply_overlay(content_obj, content_path, output_dir):
    #construct overlay
    broadcaster_name = content_obj["broadcaster_name"].replace("'", "")
    title = content_obj["title"].replace("'", "")
    overlay_text = f"{broadcaster_name}\n{title}"
    overlay = f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf:text='{overlay_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=0:y=0"
    #apply overlay 
        #--> perhaps we can also compress in this step to save time? 
    #report done or return
    # hopefully this unfucks the file recognition
    output_file = f"{output_dir}{title.replace(' ', '')}.mp4"
    os.system(f"ffmpeg -i {content_path} -vf {overlay} -codec:a copy {output_file}")
    return output_file

def compile_content(content_paths):
    # compile the given content. Maybe this should involve a strategy? 
    # for example, the strategy could determine the order of content, the length
    # of the entire video, what content to include / exclude
    for content in content_paths:
        basename = content[:-4]
        os.system(f"ffmpeg -i {content} -c:v libx264 -preset slow -crf 22 -c:a copy {basename}.mkv")
        echo = f"echo \"file '{basename}.mkv'\" >> content.txt"
        os.system(echo)

    os.system("ffmpeg -f concat -safe 0 -i content.txt compiled-vid.mp4")

# for now, just applies an overlay to all the content
def edit_content(content_dict, input_dir, output_dir):
    edited_content = []
    for content in content_dict: 
        filename = f"{content['url'].rpartition('/')[-1]}.mp4"
        content_path = f"{input_dir}{filename}"
        # apply text overlay here, other processing should happen here
        edited_path = apply_overlay(content, content_path, output_dir)
        edited_content.append(edited_path)

    return edited_content
