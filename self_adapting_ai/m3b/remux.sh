#!/bin/zsh
# Re-mux already-rendered chapters with 48 kHz audio and re-join (no re-render). usage: remux.sh standard|cloned
cd "$(dirname "$0")"; VOICE=$1; AUD=../audio_fish_s2_pro_$VOICE; OUT=out_$VOICE
: > $OUT/list.txt
for i in 01 02 03 04 05 06 07 08 09 10; do
  v=$(find media_$VOICE -name "Ch${i}_${VOICE}_final.mp4" | head -1)
  ffmpeg -v error -y -i $v -i $AUD/Scene$i.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest $OUT/ch$i.mp4
  echo "file 'ch$i.mp4'" >> $OUT/list.txt
done
ffmpeg -v error -y -f concat -safe 0 -i $OUT/list.txt -c copy ../output/Why_Brain-Like_AI_Failed_3B1B_${VOICE}.mp4
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 ../output/Why_Brain-Like_AI_Failed_3B1B_${VOICE}.mp4
