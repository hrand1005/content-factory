CLIPS="./db/tmp/*.mp4"

for file in $CLIPS
do
    echo "Formatting $file"
    basename="${file%.*}"
    # re-encode files to a consistent format
    ffmpeg -i $file -vf
    "drawtext=fontfile=/usr/share/fonts-droid-fallback/truetype/DroidSansFallback.ttf:text='TEXT':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=0:y=0"
    -codec:a copy output.mp4 
    ffmpeg -i $file -c:v libx264 -preset slow -crf 22 -c:a copy $basename.mkv
    #clips.txt used for concatenation step
    echo "file '$basename.mkv'" >> clips.txt
done
ffmpeg -f concat -safe 0 -i clips.txt compiled-vid.mp4
