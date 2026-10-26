#!/bin/zsh
# usage: finish_chapters.sh <cloned|standard> "<chapter numbers>"   — master, transcribe, render (no join)
cd "$(dirname "$0")"; V=$1; CH=(${=2})
/Users/samreedhbhuyan/dfn_venv/bin/python voice/postprocess.py $V ${CH[@]} 2>&1 | grep mastered
python3 transcribe_v2.py v3 $V 2>&1 | tail -1
ONLY=$(printf "%02d " ${CH[@]}) JOIN=0 ./render_all.sh v3$V
