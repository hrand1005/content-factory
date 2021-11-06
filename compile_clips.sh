CLIPS="./db/tmp/*.mp4"
for file in $CLIPS
do
    echo "Formatting $file"
    basename="${file%.*}"
    # re-encode files to a consistent format
    ffmpeg -i $file -c:v libx264 -preset slow -crf 22 -c:a copy $basename.mkv
    #clips.txt used for concatenation step
    echo "file '$basename.mkv'" >> clips.txt
done
ffmpeg -f concat -safe 0 -i clips.txt compiled-vid.mp4
