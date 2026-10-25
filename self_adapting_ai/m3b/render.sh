#!/bin/zsh
# usage: render.sh <chapter number> <standard|cloned> <preview|final>
set -e
cd "$(dirname "$0")"
export PATH=~/Library/TinyTeX/bin/universal-darwin:$PATH
CH=$(printf "%02d" $1); VOICE=$2; Q=${3:-preview}
if [[ $Q == final ]]; then RES="-r 1920,1080 --fps 30"; else RES="-r 854,480 --fps 15"; fi
OUT=media_$VOICE
VOICE=$VOICE manim $=RES --media_dir $OUT --progress_bar none -v WARNING ch$CH.py Ch$CH -o Ch${CH}_${VOICE}_$Q.mp4
