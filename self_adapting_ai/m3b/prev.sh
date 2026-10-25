#!/bin/zsh
# preview render + contact sheet: prev.sh <ch>
cd "$(dirname "$0")"; export PATH=~/Library/TinyTeX/bin/universal-darwin:$PATH
CH=$(printf "%02d" $1)
VOICE=${VOICE:-standard} COLUMNS=250 manim -r 854,480 --fps 15 --media_dir media_preview --progress_bar none -v WARNING ch$CH.py Ch$CH 2>&1 | grep -E "ch$CH.py|common.py|Error|error|\[late|\[cues|\[order" -A2 | head -30
f=media_preview/videos/ch$CH/480p15/Ch$CH.mp4
[[ -f $f ]] || exit 1
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f); echo "duration $d"
ffmpeg -v error -y -i $f -vf "fps=30/$d,scale=427:-1,tile=5x6" -frames:v 1 /private/tmp/claude-501/-Users-samreedhbhuyan-Desktop-Win-C-youtube-videos/182d1e3e-bb37-4f5c-ad22-6d5bb5663793/scratchpad/sheet_ch$CH.jpg
