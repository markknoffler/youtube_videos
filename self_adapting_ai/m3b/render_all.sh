#!/bin/zsh
# Final 1080p30 render of all 10 chapters for one voice, muxed with that voice's audio and concatenated.
# usage: ./render_all.sh standard|cloned
set -e
cd "$(dirname "$0")"
VOICE=${1:-standard}
AUD=../audio_fish_s2_pro_$VOICE
OUT=out_$VOICE; mkdir -p $OUT
: > $OUT/list.txt
for i in 01 02 03 04 05 06 07 08 09 10; do
  ./render.sh $i $VOICE final
  v=$(find media_$VOICE -name "Ch${i}_${VOICE}_final.mp4" | head -1)
  ffmpeg -v error -y -i $v -i $AUD/Scene$i.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest $OUT/ch$i.mp4
  rm -rf media_$VOICE/videos/ch$i/1080p30/partial_movie_files   # disk is tight
  echo "file 'ch$i.mp4'" >> $OUT/list.txt
done
ffmpeg -v error -y -f concat -safe 0 -i $OUT/list.txt -c copy ../output/Why_Brain-Like_AI_Failed_3B1B_${VOICE}.mp4
echo "done → output/Why_Brain-Like_AI_Failed_3B1B_${VOICE}.mp4"
