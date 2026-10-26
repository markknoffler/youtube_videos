#!/bin/zsh
# Final 1080p30 render of every chapter for one voice, muxed with that voice's audio and concatenated.
# usage: ./render_all.sh v2cloned|v2standard   (legacy: standard|cloned → the V1 Fish tracks)
set -e
cd "$(dirname "$0")"
VOICE=${1:-v2standard}
if [[ $VOICE == v2* ]]; then
  AUD=../audio_v2_${VOICE#v2}; CHAPTERS=(01 02 03 04 05 06 07 08 09 10 11 12); NAME=Why_Brain-Like_AI_Failed_V2_${VOICE#v2}
else
  AUD=../audio_fish_s2_pro_$VOICE; CHAPTERS=(01 02 03 04 05 06 07 08 09 10); NAME=Why_Brain-Like_AI_Failed_3B1B_${VOICE}
fi
OUT=out_$VOICE; mkdir -p $OUT
ALL=($CHAPTERS)
[[ -n $ONLY ]] && CHAPTERS=(${=ONLY})          # ONLY="01 02" renders a subset; JOIN=0 skips the final concat
for i in $CHAPTERS; do
  ./render.sh $i $VOICE final
  v=$(find media_$VOICE -name "Ch${i}_${VOICE}_final.mp4" | head -1)
  ffmpeg -v error -y -i $v -i $AUD/Scene$i.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest $OUT/ch${i}_raw.mp4
  if [[ $VOICE == v2* ]]; then
    python3 burn_captions.py $VOICE $((10#$i)) $OUT/ch${i}_raw.mp4 $OUT/ch$i.mp4 && rm $OUT/ch${i}_raw.mp4
  else
    mv $OUT/ch${i}_raw.mp4 $OUT/ch$i.mp4
  fi
  rm -rf media_$VOICE/videos/ch$i/1080p30/partial_movie_files   # disk is tight
done
[[ $JOIN == 0 ]] && exit 0
: > $OUT/list.txt
for i in $ALL; do echo "file 'ch$i.mp4'" >> $OUT/list.txt; done
CHAPTERS=($ALL)
ffmpeg -v error -y -f concat -safe 0 -i $OUT/list.txt -c copy ../output/$NAME.mp4
if [[ $VOICE == v2* ]]; then   # one SRT for the whole video, chapter offsets applied
  python3 - "$VOICE" "../output/$NAME.srt" $CHAPTERS <<'PY'
import sys, subprocess, os
sys.argv, (voice, dst, *chs) = sys.argv[:1], sys.argv[1:]
from common import caption_lines
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
off, k, out = 0.0, 1, []
for c in chs:
    for ln in caption_lines(voice, int(c)):
        out.append(f"{k}\n{ts(off + ln['s'])} --> {ts(off + ln['e'])}\n{ln['text']}\n"); k += 1
    off += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"out_{voice}/ch{c}.mp4"]))
open(dst, "w").write("\n".join(out))
PY
fi
echo "done → output/$NAME.mp4"
